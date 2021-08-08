<html>
<head>
%include header
</head>
<style>
body {background-color: pink;}

.center-screen {
  color: #1E90FF;
  font-weight: bold;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: 100vh;
}

.font{
    font-size: xx-large;
    color: #1E90FF;
    font-weight: bold;
}

.fontTwo{
    font-size: x-large;
    color: #1E90FF;
    font-weight: bold;
}

</style>
<body>
<div class="center-screen">
<p class="font">Password recovery</p>
<p class="fontTwo"></p>
<form action="/recovery" method="post">
    Username<br/>
    <input type="text" name="username"/><br/>
    <hr/>
    We will send a password reset request email to your emails inbox.
    <hr/>
    <input type="submit" value="Send Password Reset Request"/>
</form>
</div>

</body>
</html>
