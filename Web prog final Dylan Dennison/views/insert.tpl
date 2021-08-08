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
<body class="fontTwo center-screen">
<form action="/insert" method="post">
Time <input type="text" name="time"/><br>
Length <input type="text" name="length"/><br>
Side <input type="text" name="side"/><br>
Poops <input type="text" name="poops"/><br>
Pees <input type="text" name="pees"/><br>
<hr/>
<button onclick="window.location='/'; return false">Cancel</button>&nbsp
<input type="submit" value="Submit"/>
</form>
<hr/>
</body>
</html>