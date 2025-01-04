document.addEventListener('DOMContentLoaded', () => {
    if(document.querySelector("#edit_profile")){
        document.querySelector("#edit_profile").addEventListener("click", (e) => {
            const profileInfo = document.querySelector("#profile_info_div");
            const editProfile = document.querySelector("#edit_profile_div");
            profileInfo.style.display = "none";
            editProfile.style.display = "block";

            editProfile.addEventListener("click", function(e) {
                if(e.target.id === "edit_button"){
                    let featureChanged = e.target.value
                    e.target.parentElement.innerHTML = `
                        <input required id ="${featureChanged}_input" placeholder="New ${featureChanged}:">
                        <button id="save_${featureChanged}" type="submit" class ="btn btn-primary" value= ${featureChanged} >Save</button>`
                    const saveButton = document.querySelector(`#save_${featureChanged}`)
                    saveButton.addEventListener("click", () => {
                        let newContent = document.querySelector(`#${featureChanged}_input`).value;
                        if(newContent){
                            editProfileContent(featureChanged, newContent)
                        }
                        else{
                            console.log("ERROR:MUST INPUT INFORMATION")
                        }
                    })
                }
            })
        }
        )}

    const requestsContainer = document.querySelector("#friend_requests_container")
    requestsContainer.addEventListener("click", function(e)  {
        if(e.target.id === "decline_request_button"){
              const username = e.target.getAttribute("data-username");
              e.target.parentElement.parentElement.remove();
              removeRequest(username);
         }
        else if(e.target.id === "accept_request_button"){
              const username = e.target.getAttribute("data-username");
              e.target.parentElement.parentElement.remove();
              acceptRequest(username);
        }
    })
})

function editProfileContent(featureChanged, newContent) {
    fetch(`/edit_profile/${featureChanged}`,{
        method: `PUT`,
        body: JSON.stringify({
            body: newContent
        })
    })
        .then(res => res.json())
        .then(() => {
            const currentUsername = window.location.pathname.split('/').pop();
           window.location.href = `/profile/${featureChanged === "username" ? newContent : currentUsername}`;
        })
}

function removeRequest(username) {
    fetch(`/decline_friend_request/${username}`, {
        method: 'POST',
    })
}
function acceptRequest(username) {
    fetch(`/accept_friend_request_from_requests/${username}`, {
        method: 'POST',
    })
        .then(res => res.json())
        .then(() => {
            const profileInfo = document.querySelector("#profile_info_div")
            const friendsCount = parseInt(profileInfo.querySelector("#friend_count").textContent)
            profileInfo.querySelector("#friend_count").textContent = friendsCount + 1;
        })
}