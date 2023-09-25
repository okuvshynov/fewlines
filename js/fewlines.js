function _bin_index(min_val, max_val, bins, x) {
  if (min_val === max_val) {
    if (x === min_val) {
      return Math.floor(bins / 2)
    }
    return x < min_val ? 0 : bins - 1
  }
  const bin_index = Math.floor((x - min_val) * bins / (max_val - min_val));
  return Math.max(0, Math.min(bin_index, bins - 1));
}

function _histogram(values, bins, mn, mx) {
  let res = new Array(bins).fill(0);
  values.forEach(v => {
    if (!isNaN(v) && !Number.isNaN(v)) {
      res[_bin_index(mn, mx, bins, v)]++;
    }
  });
  return res;
}

function _foreach(mapLike, callback) {
  if (mapLike instanceof Map) {
    for (let [key, value] of mapLike) {
      callback(key, value);
    }
  } else if (mapLike && typeof mapLike === 'object') {
    for (let key in mapLike) {
      if (mapLike.hasOwnProperty(key)) {
        callback(key, mapLike[key]);
      }
    }
  } else {
    throw new TypeError('The provided value is neither a Map nor an object.');
  }
}

function _trim_or_pad(str, len, chr) {
  if (str.length > len) {
      return str.substr(str.length - len);
  } else {
      return chr.repeat(len - str.length) + str;
  }
}

function _header(mn, mx, bins, left_margin, show_zero=true) {
  let fmt = function(num) {
    let absNum = Math.abs(num);
    if (absNum >= 0.001 && absNum < 1000 || absNum === 0) {
        return num.toPrecision(3);
    } else {
        return num.toExponential(2);
    }
  }

  const mn_text = _trim_or_pad(" " + fmt(mn) + "|", left_margin, '~');
  let line = '~'.repeat(bins);
  if (show_zero && mn <= 0.0 && mx >= 0.0) {
    const index = _bin_index(mn, mx, bins, 0.0);
    line = line.substring(0, index) + '0' + line.substring(index + 1);
  }
  return mn_text + line + "|" + fmt(mx)
}

// expects non-negative values
export function bar_line(values) {
  const blocks = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇'];
  const max_value = Math.max(...values);
  if (max_value <= 0) {
    return "";
  }
  return values.map(v => {
    const di = Math.max(0.0, v * blocks.length / max_value);
    return blocks[Math.min(blocks.length - 1, Math.floor(di))];
  }).join("");
}

export function bar_histograms(values, bins = 60, left_margin = 20, header = true) {
  let mn = Number.POSITIVE_INFINITY;
  let mx = Number.NEGATIVE_INFINITY;
  _foreach(values, (k, v) => {
    mn = Math.min(mn, ...v);
    mx = Math.max(mx, ...v);
  });

  let res = [];

  if (header) {
    res.push(_header(mn, mx, bins, left_margin));
  }

  _foreach(values, (k, v) => {
    const hist = _histogram(v, bins, mn, mx);
    const left = _trim_or_pad(" " + k + "|", left_margin, " ");
    res.push(left + bar_line(hist) + "|");
  });

  return res
}

export function bar_histogram(values, title='', bins = 60, left_margin = 20, header = true) {
  return bar_histograms(new Map([[title, values]]), bins, left_margin, header);
}

// experiments

console.log(bar_line([1, 2, 3, 4, 4, 3, 2, 3, 3, 3, 3, 3, 33]));
bar_histograms({ 'a': [1, 23, 3, 3, 3], 'b': [2, 3, 4] }).forEach(l => console.log(l));
bar_histogram([1, 2, 3, 4, 4, 3, 2, 3, 3, 3, 3, 3, 33]).forEach(l => console.log(l));

function arrayEq(a, b) {
  return Array.isArray(a) &&
      Array.isArray(b) &&
      a.length === b.length &&
      a.every((val, index) => val === b[index]);
}

function test_bin_index() {
  console.assert(_bin_index(0, 0, 1, 0) === 0);
  console.assert(_bin_index(0, 0, 1, 10) === 0);
  console.assert(_bin_index(0, 0, 1, -10) === 0);
  
  [...Array(10).keys()].forEach(x => {
    console.assert(_bin_index(0, 10, 10, x) === x);
  });
  
  console.assert(_bin_index(0, 10, 10, 10) === 9);  

  console.assert(_bin_index(0, 10, 10, 8.9) === 8);
}

function test_header() {
  console.assert(_header(-10, 10, 20, 0) === "~~~~~~~~~~0~~~~~~~~~|10.0")
  console.assert(_header(-10, 10, 20, 10) === "~~~ -10.0|~~~~~~~~~~0~~~~~~~~~|10.0")
  console.assert(_header(-10, 10, 20, 0, false) === "~~~~~~~~~~~~~~~~~~~~|10.0")
  console.assert(_header(-10, 10, 20, 10, false) === "~~~ -10.0|~~~~~~~~~~~~~~~~~~~~|10.0")
  console.assert(_header(0, 10, 20, 0) === "0~~~~~~~~~~~~~~~~~~~|10.0")
  // TODO: formatting is bad, 0.00??
  console.assert(_header(0, 10, 20, 10) === "~~~~ 0.00|0~~~~~~~~~~~~~~~~~~~|10.0")
}

function test_bar_line() {
  console.assert(bar_line([1, 2, 3]) === "▂▅▇")
  console.assert(bar_line([]) === "")
  console.assert(bar_line([0, 100]) === " ▇")
}

function test_histogram() {
  console.assert(arrayEq(_histogram([], 5, 0, 0), [0, 0, 0, 0, 0]))
  console.assert(arrayEq(_histogram([0], 5, 0, 0), [0, 0, 1, 0, 0]))
  console.assert(arrayEq(_histogram([0, 1], 5, 0, 1), [1, 0, 0, 0, 1]))
  console.assert(arrayEq(_histogram([0], 5, 0, 1), [1, 0, 0, 0, 0]))
  console.assert(arrayEq(_histogram([0, 1, 2], 1, 0, 2), [3]))
}

function test_bar_histograms() {
  console.assert(arrayEq(bar_histograms({'A': [0], 'B': [1]}, 10, 0, false), ["▇         |", "         ▇|"]))
  console.assert(arrayEq(bar_histograms({'A': [0, 1], 'B': [1]}, 10, 0, false), ["▇        ▇|", "         ▇|"]))
  console.assert(arrayEq(bar_histograms({'A': [0, 1], 'B': [1]}, 10, 0, true), ["0~~~~~~~~~|1.00", "▇        ▇|", "         ▇|"]))
  console.assert(arrayEq(bar_histograms({'A': [0, 1], 'B': [1]}, 10, 5, true), ["0.00|0~~~~~~~~~|1.00", "   A|▇        ▇|", "   B|         ▇|"]))
}

test_bin_index()
test_header()
test_bar_line()
test_histogram()
test_bar_histograms()