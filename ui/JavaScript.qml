import QtQuick 1.0

Rectangle {
    id: dummy
    function fucking_getLength(a, b) {
        // This function is come from Sina.
        // It's the most ugly function I had been see.
        // I tried to port it to Python without success.
        // So, don't touch this magic function.
        var getLength = (function() {
            var trim = function(h) {
                try {
                    return h.replace(/^\s+|\s+$/g, "");
                } catch (j) {
                    return h;
                }
            };
            var byteLength = function(b) {
                if (typeof b == "undefined") {
                    return 0;
                }
                var a = b.match(/[^\x00-\x80]/g);
                return (b.length + (!a ? 0 : a.length));
            };


            return function(q, g) {
                g = g || {};
                g.max = g.max || 140;
                g.min = g.min || 41;
                g.surl = g.surl || 20;
                var p = trim(q).length;
                if (p > 0) {
                    var j = g.min, s = g.max, b = g.surl, n = q;
                    var r = q.match(/(http|https):\/\/[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+([-A-Z0-9a-z\$\.\+\!\_\*\(\)\/\,\:;@&=\?~#%]*)*/gi)
                    || [];
                    var h = 0;
                    for ( var m = 0, p = r.length; m < p; m++) {
                        var o = byteLength(r[m]);
                        if (/^(http:\/\/t.cn)/.test(r[m])) {
                            continue;
                        } else {
                            if (/^(http:\/\/)+(weibo.com|weibo.cn)/.test(r[m])) {
                                h += o <= j ? o : (o <= s ? b : (o - s + b));
                            } else {
                                h += o <= s ? b : (o - s + b);
                            }
                        }
                        n = n.replace(r[m], "");
                    }
                    return Math.ceil((h + byteLength(n)) / 2);
                } else {
                    return 0;
                }
            };
        })();
        return getLength(a, b)
    }
}
