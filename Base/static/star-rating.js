document.addEventListener("DOMContentLoaded", function () {

    const ratingTexts = {
        1: "Very Bad",
        2: "Bad",
        3: "Average",
        4: "Good",
        5: "Excellent"
    };

    document.querySelectorAll(".rating-selection").forEach(function (ratingBox) {

        const stars = ratingBox.querySelectorAll("i");
        const select = ratingBox.parentElement.querySelector("select[name='rating']");
        const tooltip = ratingBox.querySelector(".rating-comment-tooltip");

        function highlightStars(value) {
            stars.forEach(star => {
                const starValue = star.dataset.value;
                if (starValue <= value) {
                    star.classList.add("active", "fa-star");
                    star.classList.remove("fa-star-o");
                } else {
                    star.classList.remove("active", "fa-star");
                    star.classList.add("fa-star-o");
                }
            });
        }

        stars.forEach(star => {
            const value = star.dataset.value;

            star.addEventListener("mouseenter", () => {
                highlightStars(value);
                tooltip.textContent = ratingTexts[value];
            });

            star.addEventListener("click", () => {
                select.value = value;
                highlightStars(value);
                tooltip.textContent = ratingTexts[value];
            });
        });

        ratingBox.addEventListener("mouseleave", () => {
            const current = select.value || 0;
            highlightStars(current);
            tooltip.textContent = current ? ratingTexts[current] : "Click to rate";
        });
    });

});
