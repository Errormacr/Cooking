const server_url = localStorage.getItem('server_url');

async function fetch_recipe() {
    const query = server_url + 'recipes/' + $.urlParam('id');
    const response = await fetch(query, {
        credentials: 'include'
    });
    console.log(response);

    const recipe = await response.json();
    console.log(recipe);

}

$('document').ready(function() {
    fetch_recipe();
});