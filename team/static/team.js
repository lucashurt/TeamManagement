document.addEventListener('DOMContentLoaded', function() {
    document.querySelector("#edit_members").addEventListener('click', ()=> {
    const edit = document.getElementById('edit_container');
    if (edit.style.display === 'none') {
        edit.style.display = "block";
    }
    else {
        edit.style.display = "none";
    }
    })
    document.querySelector("#create_tasks").addEventListener('click', ()=>console.log("add"))
    document.querySelector("#edit_tasks").addEventListener('click', ()=>console.log("delete"))
    document.querySelector("#archive_project").addEventListener('click', ()=>console.log("delete"))
})

