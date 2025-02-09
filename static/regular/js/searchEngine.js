document.getElementById('search-input').addEventListener('input', function () {
    const query = this.value;
    if (query.length > 2) {
        fetch(`/search/suggestions/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                
                const suggestions = document.getElementById('suggestions');
                suggestions.innerHTML = '';
                data.forEach(suggestion => {
                    const div = document.createElement('div');
                    div.innerHTML = `<a href="${suggestion.url}">${suggestion.text}</a>`;
                    suggestions.appendChild(div);
                });
            });
    }
});