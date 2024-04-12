$(function(){
if (window.location.pathname !== "/" && window.location.pathname !== "/sign_in" && window.location.pathname !== "/sign_up" && window.location.pathname !== "/aboutme" && myuserid.innerHTML == "") {
alert("pas connecté-e vous allez être redirigé(e)")
window.location="/";
}
});
