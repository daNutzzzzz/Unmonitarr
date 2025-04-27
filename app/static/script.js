document.addEventListener('DOMContentLoaded', function() {
    // Handle rule deletion
    document.querySelectorAll('.delete-rule').forEach(button => {
        button.addEventListener('click', function() {
            const ruleId = this.getAttribute('data-id');
            fetch(`/delete_rule/${ruleId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.closest('.rule-item').remove();
                }
            });
        });
    });

    // Load quality profiles when ARR instance is selected
    const arrInstanceSelect = document.querySelector('select[name="arr_instance"]');
    if (arrInstanceSelect) {
        arrInstanceSelect.addEventListener('change', function() {
            const instanceId = this.value;
            fetch(`/get_profiles/${instanceId}`)
                .then(response => response.json())
                .then(profiles => {
                    // You could populate a dropdown or autocomplete here
                    console.log('Available profiles:', profiles);
                });
        });
    }
});