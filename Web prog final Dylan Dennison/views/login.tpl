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
    font-size: large;
    color: #1E90FF;
    font-weight: bold;
}

</style>
<body>
<div class="center-screen">
<p class="font">Welcome Back Parent!</p>
<p class="fontTwo">Sign in to access your chart!</p>
<form action="/login" method="post">
    Username<br/>
    <input type="text" name="username"/><br/>
    Password<br/>
    <input type="password" name="password"/><br/>
    <hr/>
    <input type="submit" value="Login"/>
</form>
<a href="/recovery">Click here to reset password</a><br/>
</div>

</body>
</html>



