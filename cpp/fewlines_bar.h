#ifndef __FEWLINES_BAR_H_
#define __FEWLINES_BAR_H_

#include <algorithm>
#include <array>
#include <iomanip>
#include <iostream>
#include <ranges>
#include <sstream>
#include <string>
#include <vector>
#include <optional>

namespace fewlines {

static_assert(__cplusplus >= 202002L, "fewlines requires C++ 20");


template<typename num_t>
std::optional<size_t> _bin_index_fp(num_t mn, num_t mx, size_t bins, num_t v) {
    static_assert(std::is_floating_point_v<num_t> == true);

    // sanity checks:
    if (bins == 0 || mn > mx || !std::isfinite(mn) || !std::isfinite(mx)) {
        return std::nullopt;
    }

    // corner cases
    if (v < mn) {
        return 0;
    }

    if (v > mx) {
        return bins - 1;
    }

    if (mn == mx) {
        return bins / 2;
    }

    if (bins == 1) {
        return 0;
    }

    // check for overflow of interval length
    if (mn + std::numeric_limits<num_t>::max() < mx) {
        // handle overflow: just divide everything by 2.
        mn = mn / num_t(2);
        mx = mx / num_t(2);
        // can we introduce underflow here this way? we might.
        v = v / num_t(2);
    }

    // open or closed intervals?
    auto percentile = std::max(num_t(0), (v - mn) / (mx - mn));
    size_t bin_index = bins * percentile;
    bin_index = std::min(bins - 1, bin_index);

    // this might be wrong in the underflow situation, when the interval is very large and 
    // the value is close to the boundary between buckets.
    // for example, consider mn = -1e100, mx = 1e100, bins = 2, v = -1000.
    // correct answer is 0, but we'll return 1.

    // let's try to fix that:
    auto bin_size = (mx - mn) / bins;
    auto expected_a = mn + bin_size * bin_index;
    auto expected_b = mn + bin_size * bin_index + bin_size;

    if (expected_a > v) {
        bin_index--;
    }
    if (expected_b < v) {
        bin_index++;
    }

    return std::min(bins - 1, bin_index);
}


// Assumes v is not NaN
template<typename num_t>
size_t _bin_index(num_t mn, num_t mx, size_t bins, num_t v) {
    if (std::isinf(v)) {
        return std::signbit(v) ? 0 : bins - 1;
    }
    if (mn == mx) {
        if (v == mx) {
            return bins / 2;
        }
        return v < mx ? 0 : bins - 1;
    }

    double bin = std::min(bins - 1.0, std::max(0.0, double((v - mn) * bins / (mx - mn))));
    return std::min(bins - 1, static_cast<size_t>(bin));
}

template<typename iter_t, typename num_t>
std::vector<uint64_t> _histogram(iter_t from, iter_t to, num_t mn, num_t mx, size_t bins) {
    std::vector<uint64_t> res(bins, 0ull);
    // TODO: check for mn < mx
    std::ranges::for_each(from, to, [&res, bins, mn, mx](auto v) {
        if (!std::isnan(v)) {
            res[_bin_index(mn, mx, bins, v)]++;
        }
    });
    return res;
}

std::wstring _trim_or_pad(const std::wstring& str, size_t len, wchar_t chr) {
    if (str.length() > len) {
        return str.substr(str.length() - len);
    } else {
        return std::wstring(len - str.length(), chr) + str;
    }
}

std::wstring _header(double mn, double mx, size_t bins, size_t left_margin, bool show_zero=true) {
    auto fmt = [](double v){
        std::wstringstream res;
        res << std::setprecision(3) << std::defaultfloat << v;
        return res.str();
    };
    auto mn_text = _trim_or_pad(L" " + fmt(mn) + L"|", left_margin, L'~');
    auto line = std::wstring(bins, L'~');
    if (show_zero && mn <= 0.0 && mx >= 0.0) {
        line[_bin_index(mn, mx, bins, 0.0)] = L'0';
    }
    return mn_text + line + L"|" + fmt(mx);
}

// plots a bar line with each element within provided iterator range 
// correspond to one character returned
template<typename iter_t>
std::wstring bar_line(iter_t from, iter_t to) {
    static constexpr auto blocks = std::to_array({L' ', L'▁', L'▂', L'▃', L'▄', L'▅', L'▆', L'▇'});
    auto mx_it = std::max_element(from, to);
    if (mx_it == to) {
        return L"";
    }
    auto max_value = *mx_it;
    auto block = [max_value](double v) {
        double di = v * blocks.size() / max_value;
        size_t index = std::min(blocks.size() - 1, static_cast<size_t>(std::max(0.0, di)));
        return blocks[index];
    };
    std::wstring res;
    std::ranges::transform(from, to, std::back_inserter(res), block);
    return res;
}

// plots a single histogram
template<typename iter_t>
std::wstring bar_histogram(iter_t from, iter_t to, size_t bins=60) {
    auto mx_it = std::max_element(from, to);
    auto mn_it = std::min_element(from, to);

    if (mx_it == to || mn_it == to) {
        return std::wstring(bins, L' ');
    }

    auto hist = _histogram(from, to, *mn_it, *mx_it, bins);

    return bar_line(hist.begin(), hist.end());
}

// plots a histogram with header, boundary and shared scale
// series_t can be something like 
// std::vector<std::pair<std::wstring, std::list<int>>> or std::map<std::wstring, std::vector<double>>
template<typename series_t>
std::vector<std::wstring> bar_histograms(
    const series_t& series,
    size_t bins = 60,
    size_t left_margin = 20,
    bool header = true
) {
    std::vector<std::wstring> res;
    using num_t = typename series_t::value_type::second_type::value_type; 
    num_t global_min = std::numeric_limits<num_t>::max();
    num_t global_max = std::numeric_limits<num_t>::lowest();
    for (const auto& item : series) {
        auto mx_it = std::max_element(item.second.begin(), item.second.end());
        auto mn_it = std::min_element(item.second.begin(), item.second.end());

        if (mx_it == item.second.end() || mn_it == item.second.end()) {
            continue;
        }

        global_min = std::min(global_min, *mn_it);
        global_max = std::max(global_max, *mx_it);
    }

    if (header) {
        res.push_back(_header(global_min, global_max, bins, left_margin));
    }

    for (const auto& item : series) {
        auto hist = _histogram(item.second.begin(), item.second.end(), global_min, global_max, bins);
        std::wstring left = _trim_or_pad(L" " + item.first + L"|", left_margin, L' ');
        res.push_back(left + bar_line(hist.begin(), hist.end()) + L"|");
    }
    return res;
}

}

/*

Simple demo you can compile & run as is:

$ c++ -std=c++2a -x c++ ./fewlines_bar.h -I. -D__FEWLINES_DEMO_ -o /tmp/bar_demo && /tmp/bar_demo

bar_line: 
 ▁▂▃▄▄▅▆▇▇

bar_histogram: 
                ▁▁▁▂▃▃▄▄▅▆▆▇▇▇▇▇▇▇▆▅▄▄▃▂▂▁▁▁                

empty bar_histogram: 
                                                            

bar_histograms<vector<list>>: 
~~~~~~~~~~~~~ -3.54|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~0~~~~~~~~~~~~~~~~~~~~~~~~~|2.61
~~~~~~~~~~~~~~~ one|                    ▁▁ ▁  ▁▂▁▂▆▁▁▁▂▄▄▅▇▃▂▄▁▁▅  ▄▁  ▁  ▂ ▁   |
~~~~~~~~~~~~~~~ two|         ▁  ▁  ▁▁ ▄▂▄▂▂▄▂▅▅▁▆▅▇▄▃▇▅▅▄▂▃▇▄▅▄▂▅▁ ▂▁ ▁   ▂     |

bar_histograms<map<vector>>: 
~~~~~~~~~~~~~ -3.11|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~0~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|3.16
~~~~~~~~~~~~~~ four|            ▁ ▂▂▂▂▂▄▅▅▄▅▄▅▆▅▇▄▇▅▆▅▃▂▄▆▃▄▅▁▁▂▁▁▁  ▁▁         |
~~~~~~~~~~~~~ three|        ▁     ▁▁ ▁▁▂▄▄▂▂▄▃▄▃▃▂▃▆▇▄▃▃▂▂▁▃▁▁▁▂▁ ▁  ▁  ▁   ▁   |

bar_histograms<map<set>>: 
~~~~~~~~~~~~~ -3.38|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~0~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|3.43
~~~~~~~~~~~~~~ five|          ▁   ▁▁▂▂▄▃▂▃▅▄▅▆▆▇▅▄▅▄▅▅▅▅▄▃▂▃▃▂▂▁▂▁              |
~~~~~~~~~~~~~~~ six|            ▁▁ ▂▂▂▂▃▃▅▃▄▅▅▆▇▇▅▇▇▅▅▅▅▄▃▄▁▂▄▁▄▁▁▂             |

empty bar_histograms<map<set>>: 
~~~~~~~~~~~~~~~~~ 0|0~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|1
~~~~~~~~~~~ empty A|                                                            |
~~~~~~~~~~~ empty B|                                                            |

*/

#ifdef __FEWLINES_DEMO_

#include <iostream>
#include <list>
#include <map>
#include <random>
#include <set>
#include <vector>

template<typename T>
T as(const std::vector<double>& v) {
    return T(v.begin(), v.end());
}

int main() {
    std::vector<int> v{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    std::wcout.imbue(std::locale(""));

    std::cout << std::endl << "bar_line: " << std::endl;
    std::wcout << fewlines::bar_line(v.begin(), v.end()) << std::endl;

    std::random_device rd{};
    std::mt19937 gen{rd()};

    std::normal_distribution norm_d;

    auto gen_norm = [&](size_t cnt) {
        std::vector<double> res(cnt);
        std::generate(res.begin(), res.end(), [&norm_d, &gen]{ return norm_d(gen); });
        return res;
    };

    auto v1 = gen_norm(10000);

    std::cout << std::endl << "bar_histogram: " << std::endl;
    std::wcout << fewlines::bar_histogram(v1.begin(), v1.end()) << std::endl;

    std::vector<float> empty_vector;
    std::cout << std::endl << "empty bar_histogram: " << std::endl;
    std::wcout << fewlines::bar_histogram(empty_vector.begin(), empty_vector.end()) << std::endl;

    std::vector<std::pair<std::wstring, std::list<double>>> vec1 {
        {L"one", as<std::list<double>>(gen_norm(100))},
        {L"two", as<std::list<double>>(gen_norm(200))}
    };

    std::map<std::wstring, std::vector<double>> map1 {
        {L"three", gen_norm(300)},
        {L"four", gen_norm(400)}
    };

    std::map<std::wstring, std::set<float>> map2 {
        {L"five", as<std::set<float>>(gen_norm(500))},
        {L"six", as<std::set<float>>(gen_norm(600))}
    };

    std::map<std::wstring, std::set<float>> empty_map {
        {L"empty A", {}},
        {L"empty B", {}}
    };

    std::cout << std::endl << "bar_histograms<vector<list>>: " << std::endl;

    for (auto l: fewlines::bar_histograms(vec1)) {
        std::wcout << l << std::endl;
    }
    
    std::cout << std::endl << "bar_histograms<map<vector>>: " << std::endl;

    for (auto l: fewlines::bar_histograms(map1)) {
        std::wcout << l << std::endl;
    }

    std::cout << std::endl << "bar_histograms<map<set>>: " << std::endl;
    
    for (auto l: fewlines::bar_histograms(map2)) {
        std::wcout << l << std::endl;
    }

    std::cout << std::endl << "empty bar_histograms<map<set>>: " << std::endl;
    
    for (auto l: fewlines::bar_histograms(empty_map)) {
        std::wcout << l << std::endl;
    }

    //edge_cases();

    return 0;
}

#endif


#ifdef __FEWLINES_TESTS_

#include <cassert>
#include <iostream>
#include <list>
#include <map>
#include <random>
#include <set>
#include <vector>

using namespace fewlines;

template<typename vec_t>
void plot(const vec_t& v) {
    std::wcout << fewlines::bar_histogram(v.begin(), v.end()) << std::endl;
    std::map<std::wstring, vec_t> m = { {L"vec", v} };
    for (auto l: fewlines::bar_histograms(m, 20)) {
        std::wcout << l << std::endl;
    }
}

template <typename integral_t>
void limits(const std::string& type_name) {
    std::cout << type_name << " empty:" << std::endl;
    plot(std::vector<integral_t>{});
    std::cout << type_name << " zero:" << std::endl;
    plot(std::vector<integral_t>{0});
    std::cout << type_name << " lowest:" << std::endl;
    plot(std::vector<integral_t>{std::numeric_limits<integral_t>::lowest()});
    std::cout << type_name << " max:" << std::endl;
    plot(std::vector<integral_t>{std::numeric_limits<integral_t>::max()});
    std::cout << type_name << " lowest/max:" << std::endl;
    plot(std::vector<integral_t>{std::numeric_limits<integral_t>::lowest(),
                                 std::numeric_limits<integral_t>::max()});
}

#define RUN_LIMIT(int_type) limits<int_type>(#int_type)

void edge_cases() {
    RUN_LIMIT(int8_t);
    RUN_LIMIT(uint8_t);
    RUN_LIMIT(int16_t);
    RUN_LIMIT(uint16_t);
    RUN_LIMIT(int32_t);
    RUN_LIMIT(uint32_t);
    RUN_LIMIT(int64_t);
    RUN_LIMIT(uint64_t);
    RUN_LIMIT(float);
    RUN_LIMIT(double);
    RUN_LIMIT(long double);
}

void test_bin_index() {
  assert(_bin_index(0, 0, 1, 0) == 0);
  assert(_bin_index(0, 0, 1, 10) == 0);
  assert(_bin_index(0, 0, 1, -10) == 0);
  
  for (int x = 0; x < 10; x++) {
    assert(_bin_index(0, 10, 10, x) == x);
  }
  
  assert(_bin_index(0, 10, 10, 10) == 9);  

  assert(_bin_index(0.0, 10.0, 10, 8.9) == 8);
}

void test_bin_index_fp() {
    // corner cases
    assert(_bin_index_fp(0.0, 1.0, 0, 0.5).has_value() == false);
    assert(_bin_index_fp(-std::numeric_limits<double>::infinity(), 1.0, 1, 0.5).has_value() == false);
    assert(_bin_index_fp(0.0, std::numeric_limits<double>::infinity(), 1, 0.5).has_value() == false);
    assert(_bin_index_fp(0.0, -0.1, 1, 0.5).has_value() == false);

    // values outside the interval
    assert(_bin_index_fp(0.0, 1.0, 2, 5.0) == 1);
    assert(_bin_index_fp(0.0, 1.0, 2, -5.0) == 0);
    assert(_bin_index_fp(0.0, 1.0, 2, std::numeric_limits<double>::infinity()) == 1);
    assert(_bin_index_fp(0.0, 1.0, 2, -std::numeric_limits<double>::infinity()) == 0);

    // 'normal' data
    assert(_bin_index_fp(0.0, 100.0, 10, 10.0) == 1);
    assert(_bin_index_fp(0.0, 100.0, 10, 9.999) == 0);
    assert(_bin_index_fp(0.0, 100.0, 10, 19.999) == 1);
    assert(_bin_index_fp(0.0, 100.0, 10, 100.0) == 9);
    
    // huge intervals, testing underflow
    assert(_bin_index_fp(-1.0e100, 1.0e100, 2, -10000.0) == 0);

    // overflow double
    assert(_bin_index_fp(std::numeric_limits<double>::lowest(), std::numeric_limits<double>::max(), 4, 100000.0) == 2);
    
}

void test_bar_line() {
  std::vector<int> v1{1,2,3};
  assert(bar_line(v1.begin(), v1.end()) == L"▂▅▇");
  std::vector<int> v2{};
  assert(bar_line(v2.begin(), v2.end()) == L"");
  std::vector<int> v3{0, 100};
  assert(bar_line(v3.begin(), v3.end()) == L" ▇");
}

int main() {
    std::wcout.imbue(std::locale(""));
    test_bin_index_fp();
    test_bin_index();
    test_bar_line();
    edge_cases();
    return 0;
}

#endif


#endif