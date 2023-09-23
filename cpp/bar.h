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

namespace fewlines {

static_assert(__cplusplus >= 202002L, "fewlines requires C++ 20");

template<typename iter_t>
std::vector<uint64_t> _histogram(iter_t from, iter_t to, double mn, double mx, size_t bins) {
    std::vector<uint64_t> res(bins, 0ull);
    // TODO: check for mn < mx
    std::ranges::for_each(from, to, [&res, bins, mn, mx](auto v) {
        if (!std::isnan(v)) {
            if (std::isinf(v)) {
                res[std::signbit(v) ? 0 : bins - 1]++;
            } else {
                double bin = std::min(bins - 1.0, std::max(0.0, (v - mn) * bins / (mx - mn)));
                res[std::min(bins - 1, static_cast<size_t>(bin))]++;
            }
        }
    });
    return res;
}

std::wstring _trim_or_pad(const std::wstring& str, size_t len) {
    if (str.length() > len) {
        return str.substr(str.length() - len);
    } else {
        return std::wstring(len - str.length(), L'~') + str;
    }
}

std::wstring _header(double mn, double mx, size_t bins, size_t left_margin) {
    auto fmt = [](double v){
        std::wstringstream res;
        res << std::setprecision(3) << std::defaultfloat << v;
        return res.str();
    };
    auto mn_text = _trim_or_pad(L" " + fmt(mn) + L"|", left_margin);

    return mn_text + std::wstring(bins, L'~') + L"|" + fmt(mx);
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
    num_t global_max = std::numeric_limits<num_t>::min();
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
        std::wstring left = _trim_or_pad(L" " + item.first + L"|", left_margin);
        res.push_back(left + bar_line(hist.begin(), hist.end()) + L"|");
    }
    return res;
}

}

// Simple demo you can compile & run as is:
// c++ -std=c++2a -x c++ ./bar.h -I. -D__FEWLINES_DEMO_ -o ./bar_demo

/*

bar_line: 
▂▄▆▇

bar_histogram: 
▇                   ▇                   ▇                  ▇

bar_histograms<vector<list>>: 
~~~~~~~~~~~~~~~~~ 1|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|6
~~~~~~~~~~~~~~~ one|▇           ▇           ▇                                   |
~~~~~~~~~~~~~~~ two|                                    ▇           ▇          ▇|

bar_histograms<map<vector>>: 
~~~~~~~~~~~~~~~ 7.1|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|12.6
~~~~~~~~~~~~~~ four|                                    ▇           ▇          ▇|
~~~~~~~~~~~~~ three|▇          ▇            ▇                                   |

bar_histograms<map<set>>: 
~~~~~~~~~~~~~~ 13.7|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|18.2
~~~~~~~~~~~~~~ five|▇             ▇              ▇                              |
~~~~~~~~~~~~~~~ six|                              ▇              ▇             ▇|

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

    return 0;
}

#endif
#endif