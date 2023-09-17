function copyUrlToClipboard() {
    var url = window.location.href;

    var input = document.createElement('input');
    input.setAttribute('value', url);
    document.body.appendChild(input);

    input.select();
    input.setSelectionRange(0, 99999);

    document.execCommand('copy');

    document.body.removeChild(input);

    alert('URL copied to clipboard: ' + url);
}
