<title>Newborn Chart</title>
<meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Outlined" rel="stylesheet">

  <script src="https://www.gstatic.com/charts/loader.js"></script>
  <script>
    google.charts.load('current', {packages: ['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
      
      var data = google.visualization.arrayToDataTable([
         ["Element", "Number of Bowel Movements", { role: "style" } ],
         ['Day 1', 1.00, 'black'],
         ['Day 2', 1.00, 'black'],           
         ['Day 3', 1.00, 'green'],            
         ['Day 4', 4.00, 'green'],
         ['Day 5', 4.00, 'yellow' ],
         ['Day 6', 5.00, 'yellow' ],  
      ]);

      
      var chart = new google.visualization.BarChart(document.getElementById('myPieChart'));
      chart.draw(data, null);
    }
  </script>
