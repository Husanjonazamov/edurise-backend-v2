document.addEventListener("DOMContentLoaded", function () {
    IMask(document.getElementById("regexp-mask"), {mask: /^[1-6]\d{0,5}$/}),

        IMask(document.getElementById("phone-mask"), {mask: "+{998}(00)000-00-00"}),

        IMask(document.getElementById("number-mask"), {mask: Number, min: -1e4, max: 1e4, thousandsSeparator: " "}),
        IMask(document.getElementById("date-mask"), {
            mask: Date, min: new Date(1990, 0, 1), max: new Date(2020, 0, 1), lazy: !1
        }),

        IMask(document.getElementById("dynamic-mask"),
        {mask: [{mask: "+{998}(00)000-00-00"}, {mask: /^\S*@?\S*$/}]}),

        IMask(document.getElementById("currency-mask"), {
            mask: "$num",
            blocks: {num: {mask: Number, thousandsSeparator: " "}}
        })
});