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
<p class="font">Welcome Back!</p>
<p class="fontTwo">Reset Password</p>
<form action="/reset/{{username}}/{{reset_token}}" method="post">
    Username<br/>
    <p>{{ username }}</p><br/>
    Password<br/>
    <input type="password" name="password"/><br/>
    Password<br/>
    <input type="password" name="password_again"/><br/>
    <hr/>
    <input type="submit" value="Reset Password"/>
    <input type="hidden" name="csrf_token" value="{{csrf_token}}"/>
</form>
</div>

</body>
</html>