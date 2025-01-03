document.addEventListener('DOMContentLoaded', () => {
    if(document.querySelector("#edit_profile")){
        document.querySelector("#edit_profile").addEventListener("click", (e) => {console.log("banana!")}
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

function removeRequest(username) {
    fetch(`/decline_friend_request/${username}`, {
        method: 'POST',
    })
}
function acceptRequest(username) {
    fetch(`/accept_friend_request/${username}`, {
        method: 'POST',
    })
        .then(res => res.json())
        .then(() => {
            const profileInfo = document.querySelector("#profile_info_div")
            const friendsCount = parseInt(profileInfo.querySelector("#friend_count").textContent)
            profileInfo.querySelector("#friend_count").textContent = friendsCount + 1;
        })
}