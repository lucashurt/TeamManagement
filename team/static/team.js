document.addEventListener('DOMContentLoaded', function() {
    const currentMembersContainer = document.getElementById('current_members');
    const addMembersSelector = document.getElementById('add_member_select');
    const addMemberButton = document.getElementById('add_member');

    document.querySelector("#edit_members").addEventListener('click', ()=> {
    const edit = document.getElementById('edit_container');
    if (edit.style.display === 'none') {
        edit.style.display = "block";
    }
    else {
        edit.style.display = "none";
    }
    })
    currentMembersContainer.addEventListener('click', function(e) {
        if(e.target.id === 'delete_member') {
            const username = e.target.getAttribute('data-username');
            e.target.parentElement.remove();
            removeMember(username);
        }
    })
    document.querySelector("#create_tasks").addEventListener('click', ()=>console.log("add"))
    document.querySelector("#edit_tasks").addEventListener('click', ()=>console.log("delete"))
    document.querySelector("#archive_project").addEventListener('click', ()=>console.log("delete"))
})
function removeMember(username){
    let team_name = document.getElementById('team_name').innerText;
    fetch(`/edit_members/${team_name}`,{
        method: 'POST',
        body: JSON.stringify({
            remove: username
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.error){
                console.log(data.error)
            }
        })
}