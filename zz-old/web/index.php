<!DOCTYPE html>
<html>

  <head>
    <title>LED Controller</title>
  </head>

  <body>
    <p>LEDs now showing: 
      <?php
        if(isset($_GET['mode'])) {
          echo " {$_GET['mode']}";
          $file = fopen("mode.html", 'w');
          fwrite($file, $_GET['mode']);
          if($_GET['mode']=="Solid" && isset($_GET['r']) && isset($_GET['g']) && isset($_GET['b'])) {
            fwrite($file, "\n".(int)$_GET['r']."\n".(int)$_GET['g']."\n".(int)$_GET['b']);
          } else if ($_GET['mode']=="Custom" && isset($_GET['value'])) {
            fwrite($file, "\n".$_GET['value']);
          }
          fclose($file);
        }
      ?>
    </p>

    <form action="" method="get">
      <input type="submit" name="mode" value="Clock"><br/>
      <input type="submit" name="mode" value="Bounce"><br/>
      <input type="submit" name="mode" value="Off"><br/>
    </form>

    <form action="upload.php" method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <button type="submit" name="submit">Upload</button>
    </form>

  </body>

</html>
