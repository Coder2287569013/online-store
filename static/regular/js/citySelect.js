document.getElementById('region_id').addEventListener('change', function () {
    const regionId = this.value;
    const citySelect = document.getElementById('id_city');
    citySelect.innerHTML = '<option value="">--- Select a city ---</option>';
    if (regionId) {
        fetch(`../create/cities/?region_id=${regionId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch cities');
            }
            return response.json();
        })
            .then(data => {
                data.forEach(city => {
                    const option = document.createElement('option');
                    option.value = city.id;
                    option.textContent = city.name;
                    citySelect.appendChild(option);
                });
            });
    }
});