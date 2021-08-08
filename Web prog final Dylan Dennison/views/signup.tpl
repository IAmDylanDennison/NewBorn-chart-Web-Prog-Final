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
<p class="font">Welcome!</p>
<p class="fontTwo">Sign Up to chart your new baby!</p>
<form action="/signup" method="post">
    Username<br/>
    <input type="text" name="username"/><br/>
    Password<br/>
    <input type="password" name="password"/><br/>
    Password<br/>
    <input type="password" name="password_again"/><br/>
    Email<br/>
    <input type="text" name="email"/><br/>
    <hr/>
    <input type="submit" value="Sign Up"/>
</form>

</div>

</body>
</html>