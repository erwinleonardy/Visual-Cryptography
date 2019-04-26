// executes when the document is ready
$(document).ready()
{
  // get the display name
  var strRes = document.getElementById('displayName');

  // modify the display name if it is too long
  if (strRes != null)
  {
    var username = strRes.innerHTML;
    strRes.innerHTML = shortenUsername(username)
  }
}

// this function allows usernames which
// are longer than 15 characters to be shrunk
// to 15 characters
function shortenUsername(username) 
{
  if (username.length > 15)
    return username.substring(0, username.length - 3) + "...";
  else
    return username;
}