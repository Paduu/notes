function set_cookie() {
    passin = prompt("Please enter the Key: ");
    var myDate = new Date();
    myDate.setDate(myDate.getDate() + 1);
    myDate.setHours(09,0,0,0);
    var passenc = window.btoa(passin);
    var cookieName = 'notescookie';
    var cookieValue = passenc ;
    document.cookie = cookieName +"=" + cookieValue + ";expires=" + myDate + "; domain=notes-python.herokuapp.com; path=/;";
    location.reload();
}

function delete_cookie() {
    var cookieName = 'notescookie';
    document.cookie = cookieName +"=; expires=Thu, 01 Jan 1970 00:00:00 UTC; domain=notes-python.herokuapp.com; path=/;";
    location.reload();
}

function notes_dec () {
    var noteskey = window.atob(document.cookie.split("=")[1])
    var noteenc = window.atob(document.getElementsByName("note")[0].value);
    var notedec = CryptoJS.AES.decrypt(noteenc, noteskey).toString(CryptoJS.enc.Utf8);
    document.getElementsByName("note")[0].value = notedec;

}

function notes_enc () {
    var noteskey = window.atob(document.cookie.split("=")[1])
    var plain = document.getElementsByName("note")[0].value
    var encrypted = CryptoJS.AES.encrypt(plain, noteskey);
    document.getElementsByName("note")[0].value = window.btoa(encrypted);
    
}

function checkCookie () {
    var notescookie = document.cookie;
    if (notescookie) {
        document.getElementById("deleteKey").style.display = "block";
        notes_dec();
    } else {
        document.getElementById("addKey").style.display = "block";
    }
}
