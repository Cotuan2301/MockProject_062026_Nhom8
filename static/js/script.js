var Bizweb = Bizweb || {};
Bizweb.store = 'bean-spa.mysapo.net';
Bizweb.id = 632411;
Bizweb.theme = { "id": 1096693, "name": "Bean Spa", "role": "main" };
Bizweb.template = 'customers/login';
if (!Bizweb.fbEventId) Bizweb.fbEventId = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
});


(function () {
    function asyncLoad() {
        var urls = [];
        for (var i = 0; i < urls.length; i++) {
            var s = document.createElement('script');
            s.type = 'text/javascript';
            s.async = true;
            s.src = urls[i];
            var x = document.getElementsByTagName('script')[0];
            x.parentNode.insertBefore(s, x);
        }
    };
    window.attachEvent ? window.attachEvent('onload', asyncLoad) : window.addEventListener('load', asyncLoad, false);
})();


window.BizwebAnalytics = window.BizwebAnalytics || {};
window.BizwebAnalytics.meta = window.BizwebAnalytics.meta || {};
window.BizwebAnalytics.meta.currency = 'VND';
window.BizwebAnalytics.tracking_url = '/s';

var meta = {};


for (var attr in meta) {
    window.BizwebAnalytics.meta[attr] = meta[attr];
}


document.addEventListener('DOMContentLoaded', function () {
    awe_lazyloadImage();
    /*Header promotion*/

    function getItemSearch(name, smartjson) {
        return fetch(`https://${window.location.hostname}/search?q=${name}&view=${smartjson}&type=product`)
            .then(res => res.json())
            .catch(err => console.error(err));
    }

    var searchRecent = document.querySelector('.search-suggest .search-recent');
    var searchRecentList = localStorage.getItem('search_recent_list');
    var recentList = searchRecentList ? JSON.parse(searchRecentList) : [];

    if (recentList.length > 0) {
        searchRecent.classList.remove('d-none');
        var searchList = searchRecent.querySelector('.search-list');
        recentList.forEach(function (item) {
            var link = document.createElement('a');
            link.href = `/search?query=${encodeURIComponent(item)}&type=product`;
            link.textContent = item;
            link.title = `Tìm kiếm ${item}`;
            link.classList.add('search-item');

            var closeSpan = document.createElement('span');
            closeSpan.textContent = 'Đóng';
            closeSpan.title = 'Đóng';
            closeSpan.classList.add('close');

            closeSpan.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                var index = recentList.indexOf(item);
                if (index !== -1) {
                    recentList.splice(index, 1);
                    localStorage.setItem('search_recent_list', JSON.stringify(recentList));
                    searchList.removeChild(link);
                    if (recentList.length == 0) {
                        searchRecent.classList.toggle('d-none');
                    }
                }
            });

            link.appendChild(closeSpan);
            searchList.appendChild(link);
        });
    }

    var searchInput = document.querySelectorAll('.header_tim_kiem input[type="text"], .search-mobile input[type="text"]');
    searchInput.forEach(function (input) {
        input.addEventListener('keyup', function (e) {
            let term = this.value.trim();
            let data = '';
            var resultbox = '';
            if (term.length > 1) {
                searchRecent.classList.add('d-none');

                async function goawaySearch() {
                    data = await getItemSearch(term, 'smartjson');
                    setTimeout(function () {
                        var sizeData = Object.keys(data).length;
                        if (sizeData > 0) {
                            Object.keys(data).forEach(function (key) {
                                if (data[key].compare_price !== 0) {
                                    resultbox += `<a class="product-smart" href="${data[key].url}" title="${data[key].name}"><div class="image_thumb"><img width="58" height="58" class="lazyload loaded" src="${data[key].image}" data-src="${data[key].image}" alt="${data[key].name}" data-was-processed="true"></div><div class="product-info"><h3 class="product-name"><span>${data[key].name}</span></h3><div class="price-box"><span class="price">${data[key].price}</span><span class="compare-price">${data[key].compare_price}</span></div></div></a>`;
                                } else {
                                    resultbox += `<a class="product-smart" href="${data[key].url}" title="${data[key].name}"><div class="image_thumb"><img width="58" height="58" class="lazyload loaded" src="${data[key].image}" data-src="${data[key].image}" alt="${data[key].name}" data-was-processed="true"></div><div class="product-info"><h3 class="product-name"><span>${data[key].name}</span></h3><div class="price-box"><span class="price">${data[key].price}</span></div></div></a>`;
                                }
                            });
                            resultbox += `<a href="/search?query=${term}&type=product" class="see-all-search" title="Xem tất cả">Xem tất cả kết quả »</a>`;
                            document.querySelector('.list-search').innerHTML = resultbox;
                        } else {
                            document.querySelector('.list-search').innerHTML = '<div class="not-pro">Không có thấy kết quả tìm kiếm</div>';
                        }
                    }, 200);
                }

                goawaySearch();
            } else {
                if (recentList.length > 0) {
                    searchRecent.classList.remove('d-none');
                }
                document.querySelector('.list-search').innerHTML = '';
            }
        });
    });


    function getItemSearchCompare(name, smartjsonpro) {
        return fetch(`https://${window.location.hostname}/search?q=name:(*${name}*)&view=${smartjsonpro}&type=product`)
            .then(res => res.json())
            .catch(err => console.error(err))
    }
    $('.header_compare input[type="text"]').bind('keyup change', function (e) {
        let termcom = $(this).val().trim();
        let datacom = '';
        var resultboxcom = '';
        if (termcom.length > 1) {
            async function goawaySearchcom() {
                datacom = await getItemSearchCompare(termcom, 'smartjsonpro');
                setTimeout(function () {
                    var sizeDatacom = Object.keys(datacom).length;
                    if (sizeDatacom > 0) {
                        Object.keys(datacom).forEach(function (key) {
                            if (datacom[key].compare_price != 0 && datacom[key].type != '') {
                                resultboxcom += `<div class="product-smart"><a class="image_thumb" href="${datacom[key].url}" title="${datacom[key].name}"><img width="480" height="480" class="lazyload loaded" src="${datacom[key].image}" data-src="${datacom[key].image}" alt="${datacom[key].name}" data-was-processed="true"></a><div class="product-info"><h3 class="product-name"><a href="${datacom[key].url}">${datacom[key].name}</a></h3><div class="price-box"><span class="price">${datacom[key].price}</span><span class="compare-price">${datacom[key].compare_price}</span></div><a href="javascript:void(0)" class="setCompare btn-views js-compare-product-add" data-compare="${datacom[key].alias}" data-type="${datacom[key].type}" tabindex="0" title="So sánh"><svg enable-background="new 0 0 128 128" height="512" viewBox="0 0 128 128" width="512" xmlns="http://www.w3.org/2000/svg"><path id="Random" d="m31.648 40h-19.648c-2.209 0-4-1.791-4-4s1.791-4 4-4h19.648c9.021 0 17.541 4.383 22.785 11.725l4.651 6.511-4.916 6.882-6.245-8.743c-3.745-5.244-9.829-8.375-16.275-8.375zm87.18 49.172-16-16c-1.563-1.563-4.094-1.563-5.656 0s-1.563 4.094 0 5.656l9.172 9.172h-9.992c-6.445 0-12.529-3.131-16.275-8.375l-6.245-8.743-4.916 6.882 4.651 6.511c5.244 7.342 13.763 11.725 22.785 11.725h9.992l-9.172 9.172c-1.563 1.563-1.563 4.094 0 5.656.781.781 1.805 1.172 2.828 1.172s2.047-.391 2.828-1.172l16-16c1.563-1.562 1.563-4.094 0-5.656zm0-56-16-16c-1.563-1.563-4.094-1.563-5.656 0s-1.563 4.094 0 5.656l9.172 9.172h-9.992c-9.021 0-17.541 4.383-22.787 11.727l-25.639 35.896c-3.748 5.246-9.832 8.377-16.278 8.377h-19.648c-2.209 0-4 1.791-4 4s1.791 4 4 4h19.648c9.021 0 17.541-4.383 22.787-11.727l25.639-35.896c3.748-5.246 9.832-8.377 16.278-8.377h9.992l-9.172 9.172c-1.563 1.563-1.563 4.094 0 5.656.781.781 1.805 1.172 2.828 1.172s2.047-.391 2.828-1.172l16-16c1.563-1.562 1.563-4.094 0-5.656z"/> </svg> </a></div></div>`
                            } else if (datacom[key].compare_price != 0 && datacom[key].type == '') {
                                resultboxcom += `<div class="product-smart"><a class="image_thumb" href="${datacom[key].url}" title="${datacom[key].name}"><img width="480" height="480" class="lazyload loaded" src="${datacom[key].image}" data-src="${datacom[key].image}" alt="${datacom[key].name}" data-was-processed="true"></a><div class="product-info"><h3 class="product-name"><a href="${datacom[key].url}">${datacom[key].name}</a></h3><div class="price-box"><span class="price">${datacom[key].price}</span><span class="compare-price">${datacom[key].compare_price}</span></div><a href="javascript:void(0)" class="setCompare btn-views js-compare-product-add" data-compare="${datacom[key].alias}" data-type="default-type" tabindex="0" title="So sánh"><svg enable-background="new 0 0 128 128" height="512" viewBox="0 0 128 128" width="512" xmlns="http://www.w3.org/2000/svg"><path id="Random" d="m31.648 40h-19.648c-2.209 0-4-1.791-4-4s1.791-4 4-4h19.648c9.021 0 17.541 4.383 22.785 11.725l4.651 6.511-4.916 6.882-6.245-8.743c-3.745-5.244-9.829-8.375-16.275-8.375zm87.18 49.172-16-16c-1.563-1.563-4.094-1.563-5.656 0s-1.563 4.094 0 5.656l9.172 9.172h-9.992c-6.445 0-12.529-3.131-16.275-8.375l-6.245-8.743-4.916 6.882 4.651 6.511c5.244 7.342 13.763 11.725 22.785 11.725h9.992l-9.172 9.172c-1.563 1.563-1.563 4.094 0 5.656.781.781 1.805 1.172 2.828 1.172s2.047-.391 2.828-1.172l16-16c1.563-1.562 1.563-4.094 0-5.656zm0-56-16-16c-1.563-1.563-4.094-1.563-5.656 0s-1.563 4.094 0 5.656l9.172 9.172h-9.992c-9.021 0-17.541 4.383-22.787 11.727l-25.639 35.896c-3.748 5.246-9.832 8.377-16.278 8.377h-19.648c-2.209 0-4 1.791-4 4s1.791 4 4 4h19.648c9.021 0 17.541-4.383 22.787-11.727l25.639-35.896c3.748-5.246 9.832-8.377 16.278-8.377h9.992l-9.172 9.172c-1.563 1.563-1.563 4.094 0 5.656.781.781 1.805 1.172 2.828 1.172s2.047-.391 2.828-1.172l16-16c1.563-1.562 1.563-4.094 0-5.656z"/> </svg></a></div></div>`
                            } else if (datacom[key].compare_price == 0 && datacom[key].type != '') {
                                resultboxcom += `<div class="product-smart"><a class="image_thumb" href="${datacom[key].url}" title="${datacom[key].name}"><img width="480" height="480" class="lazyload loaded" src="${datacom[key].image}" data-src="${datacom[key].image}" alt="${datacom[key].name}" data-was-processed="true"></a><div class="product-info"><h3 class="product-name"><a href="${datacom[key].url}">${datacom[key].name}</a></h3><div class="price-box"><span class="price">${datacom[key].price}</span></div><a href="javascript:void(0)" class="setCompare btn-views js-compare-product-add" data-compare="${datacom[key].alias}" data-type="${datacom[key].type}" tabindex="0" title="So sánh"><svg enable-background="new 0 0 128 128" height="512" viewBox="0 0 128 128" width="512" xmlns="http://www.w3.org/2000/svg"><path id="Random" d="m31.648 40h-19.648c-2.209 0-4-1.791-4-4s1.791-4 4-4h19.648c9.021 0 17.541 4.383 22.785 11.725l4.651 6.511-4.916 6.882-6.245-8.743c-3.745-5.244-9.829-8.375-16.275-8.375zm87.18 49.172-16-16c-1.563-1.563-4.094-1.563-5.656 0s-1.563 4.094 0 5.656l9.172 9.172h-9.992c-6.445 0-12.529-3.131-16.275-8.375l-6.245-8.743-4.916 6.882 4.651 6.511c5.244 7.342 13.763 11.725 22.785 11.725h9.992l-9.172 9.172c-1.563 1.563-1.563 4.094 0 5.656.781.781 1.805 1.172 2.828 1.172s2.047-.391 2.828-1.172l16-16c1.563-1.562 1.563-4.094 0-5.656zm0-56-16-16c-1.563-1.563-4.094-1.563-5.656 0s-1.563 4.094 0 5.656l9.172 9.172h-9.992c-9.021 0-17.541 4.383-22.787 11.727l-25.639 35.896c-3.748 5.246-9.832 8.377-16.278 8.377h-19.648c-2.209 0-4 1.791-4 4s1.791 4 4 4h19.648c9.021 0 17.541-4.383 22.787-11.727l25.639-35.896c3.748-5.246 9.832-8.377 16.278-8.377h9.992l-9.172 9.172c-1.563 1.563-1.563 4.094 0 5.656.781.781 1.805 1.172 2.828 1.172s2.047-.391 2.828-1.172l16-16c1.563-1.562 1.563-4.094 0-5.656z"/> </svg></a></div></div>`
                            } else {
                                resultboxcom += `<div class="product-smart"><a class="image_thumb" href="${datacom[key].url}" title="${datacom[key].name}"><img width="480" height="480" class="lazyload loaded" src="${datacom[key].image}" data-src="${datacom[key].image}" alt="${datacom[key].name}" data-was-processed="true"></a><div class="product-info"><h3 class="product-name"><a href="${datacom[key].url}">${datacom[key].name}</a></h3><div class="price-box"><span class="price">${datacom[key].price}</span></div><a href="javascript:void(0)" class="setCompare btn-views js-compare-product-add" data-compare="${datacom[key].alias}" data-type="default-type" tabindex="0" title="So sánh"><svg enable-background="new 0 0 128 128" height="512" viewBox="0 0 128 128" width="512" xmlns="http://www.w3.org/2000/svg"><path id="Random" d="m31.648 40h-19.648c-2.209 0-4-1.791-4-4s1.791-4 4-4h19.648c9.021 0 17.541 4.383 22.785 11.725l4.651 6.511-4.916 6.882-6.245-8.743c-3.745-5.244-9.829-8.375-16.275-8.375zm87.18 49.172-16-16c-1.563-1.563-4.094-1.563-5.656 0s-1.563 4.094 0 5.656l9.172 9.172h-9.992c-6.445 0-12.529-3.131-16.275-8.375l-6.245-8.743-4.916 6.882 4.651 6.511c5.244 7.342 13.763 11.725 22.785 11.725h9.992l-9.172 9.172c-1.563 1.563-1.563 4.094 0 5.656.781.781 1.805 1.172 2.828 1.172s2.047-.391 2.828-1.172l16-16c1.563-1.562 1.563-4.094 0-5.656zm0-56-16-16c-1.563-1.563-4.094-1.563-5.656 0s-1.563 4.094 0 5.656l9.172 9.172h-9.992c-9.021 0-17.541 4.383-22.787 11.727l-25.639 35.896c-3.748 5.246-9.832 8.377-16.278 8.377h-19.648c-2.209 0-4 1.791-4 4s1.791 4 4 4h19.648c9.021 0 17.541-4.383 22.787-11.727l25.639-35.896c3.748-5.246 9.832-8.377 16.278-8.377h9.992l-9.172 9.172c-1.563 1.563-1.563 4.094 0 5.656.781.781 1.805 1.172 2.828 1.172s2.047-.391 2.828-1.172l16-16c1.563-1.562 1.563-4.094 0-5.656z"/> </svg></a></div></div>`
                            }
                        });
                        $('.list-compare').html(resultboxcom);
                    } else {
                        $('.list-compare').html('<div class="not-pro">Không có thấy kết quả tìm kiếm</div>');
                    }
                }, 500);
            }
            goawaySearchcom();
            setTimeout(function () {
                beanComprare.Compare.compareProduct();
            }, 1000);
        } else {
            $('.list-compare').html('');
        }
    });

});
function awe_lazyloadImage() {
    var ll = new LazyLoad({
        elements_selector: ".lazyload",
        load_delay: 100,
        threshold: 0
    });
} window.awe_lazyloadImage = awe_lazyloadImage;