function debounce(func, delay) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

document.getElementById('search-input').addEventListener('input', debounce(function () {
    const query = this.value.trim();
    const suggestions = document.getElementById('suggestions');

    if (query.length > 2) {
        fetch(`/search/suggestions/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                suggestions.innerHTML = '';
                data.forEach(suggestion => {
                    const div = document.createElement('div');
                    div.innerHTML = `<a href="${suggestion.url}">${suggestion.text}</a>`;
                    suggestions.appendChild(div);
                });
                suggestions.classList.add('show');
            })
            .catch(error => console.error('Error fetching suggestions:', error));
    } else {
        suggestions.innerHTML = '';
        suggestions.classList.remove('show');
    }
}, 300));