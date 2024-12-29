document.addEventListener('DOMContentLoaded', function() {
    const currentMembersContainer = document.getElementById('current_members');
    const addMembersSelector = document.getElementById('add_member_select');
    const addMemberButton = document.getElementById('add_member_button');

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
    addMemberButton.addEventListener('click', () => {
        const selectedOption = addMembersSelector.options[addMembersSelector.selectedIndex];
        const username =selectedOption.textContent;
        const userID = selectedOption.value;
        addMember(username,userID)})

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
            const addMembersSelector = document.getElementById('add_member_select');
            const newOption = document.createElement('option');
            newOption.value=username
            newOption.textContent=username
            addMembersSelector.appendChild(newOption)
            if (data.error){
                console.log(data.error)
            }
        })
}

function addMember(username,userID){
    let team_name = document.getElementById('team_name').innerText;
    fetch(`/edit_members/${team_name}`,{
        method: 'POST',
        body: JSON.stringify({
            "add": username
        })
    })
        .then(res => res.json())
        .then(data => {
            const currentMembersContainer = document.getElementById('current_members');

            const newMemberRow = document.createElement('div');
            newMemberRow.className = "row"
            newMemberRow.style = 'justify-content:space-between;margin:30px'

            const deleteButton = document.createElement('button');
            deleteButton.id = "delete_member";
            deleteButton.className = 'btn btn-outline-danger';
            deleteButton.setAttribute('data-username', username);
            deleteButton.textContent = 'Delete Member';

            const newMember = document.createElement("span")
            newMember.textContent = username


            newMemberRow.appendChild(newMember);
            newMemberRow.appendChild(deleteButton);
            currentMembersContainer.appendChild(newMemberRow);
            currentMembersContainer.appendChild(document.createElement('hr'))

            const addMemberSelector = document.getElementById('add_member_select');
            addMemberSelector.querySelector(`option[value="${userID}"]`).remove();
        })
}