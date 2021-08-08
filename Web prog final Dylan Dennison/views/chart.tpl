<!DOCTYPE html>
<html>
<head>
%include header
</head>
<style>
body {background-color: pink;}

.center-screen {
  color: #89CFF0;
  font-weight: bold;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: 100vh;
}

.center-button {
  color: #89CFF0;
  font-weight: bold;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.font{
    font-size: xx-large;
    color: #1E90FF;
    font-weight: bold;
}

.fontTwo{
    font-size: x-large;
    color: #1E90FF !important;
    font-weight: bold;
}

.fontThree{
    font-size: medium;
    color: #1E90FF !important;
    font-weight: bold;
}

.navBar{
    background-color: pink !important;
    font-size: large;
    color: #1E90FF !important;
   
}
 .banner{
     background-color: #1E90FF !important;
     font-size: large;
     color: pink !important;
 }

 .footer {
    clear: both;
    position: relative;
    height: 200px;
    margin-top: -200px;
}
</style>
<body>
%if message:
  %include('alert.tpl', message=message) 
%end
<p class="fontThree center-button">Please Login to Chart</p>
<span class="fontThree">
<hr/>
<nav class="navbar navbar-expand-sm  justify-content-center navBar">
  <ul class="navbar-nav">
    <li class="nav-item">
      <a class="nav-link" href="/login">Login</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" href="/signup">Sign Up</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" href="/logout">Logout</a>
    </li>
  </ul>
</nav>
<hr/>
</span>

<div class="jumbotron text-center banner m-5 py-5">
  <h1>Newborn Chart</h1>
  <p>A new way to keep track of your baby!</p> 
  <img src="/static/babychart.png" class="rounded" alt="Baby toy"/>
</div>



<table class="table table-hover">
  <tr>
    <th></th>
    <th>Time</th>
    <th>Length</th>
    <th>Side</th>
    <th>Poops</th>
    <th>Pees</th>
    <th></th>
    <th></th>
  </tr>
  %for item in itemsInDatabase:
    <tr>
      <th> </th>
      <td>{{item['time']}}</td>
      <td>{{item['length']}}</td>
      <td>{{item['side']}}</td>
      <td>{{item['poops']}}</td>
      <td>{{item['pees']}}</td>
      <td><a href="/edit/{{item['id']}}"><span class="fontThree">
Edit
</span></a></td>
      <td><a href="/delete/{{item['id']}}"><span class="fontThree">
Delete
</span></a></td>
    </tr>
  %end
</table>
<hr/>
<span class="fontThree center-button"><a href="insert">Add New Feed Time</a></span>






<div class="row m-5 py-5">
    <div class="col fontThree">
    <span class="fontTwo">Think something is wrong with your newborn?<br/>
    Please click the links below.<br/></span>
     <a href="https://www.healthychildren.org/English/Pages/default.aspx">healthychildren.org</a><br/>
     <a href="https://www.aap.org/en-us/Pages/Default.aspx">aap.org</a><br/>
     <a href="https://www.uclahealth.org/mattel/workfiles/newborn-manual/NewbornHandbookChapter3.pdf">uclahealth.org</a>
    </div>
    <div class="col">
      <span class="fontTwo">Bowel Movement Chart<br/>
      <div id="myPieChart"/>
    </div>
</div>


</body>
</html>