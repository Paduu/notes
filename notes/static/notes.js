function set_cookie() {
    passin = prompt("Please enter the Key: ");
    var myDate = new Date();
    myDate.setDate(myDate.getDate() + 1);
    myDate.setHours(09,0,0,0);
    var passenc = window.btoa(passin);
    var cookieName = 'notescookie';
    var cookieValue = passenc ;
    document.cookie = cookieName +"=" + cookieValue + ";expires=" + myDate + ";domain=notes-python.herokuapp.com;path=/";
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
        notes_dec();
    } else {
        set_cookie();
    }
}