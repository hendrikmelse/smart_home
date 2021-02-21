<?php
if (isset($_POST['submit'])) {
    $file = $_FILES['file'];

    $file_name = $_FILES['file']['name'];
    $file_tmp_name = $_FILES['file']['tmp_name'];
    $file_size = $_FILES['file']['size'];
    $file_error = $_FILES['file']['error'];
    $file_type = $_FILES['file']['type'];
    
    $file_ext = strtolower(end(explode('.', $file_name)));

    $allowed = array('txt', 'jpg', 'jpeg', 'png');

    if (in_array($file_ext, $allowed)) {
        if ($file_error === 0) {
            if ($file_size < 1000000) {
                $file_name_new = "image." . $file_ext;
                $file_destination = 'uploads/' . $file_name_new;
                move_uploaded_file($file_tmp_name, $file_destination);
                echo "Image uploaded successfully";
                //header("Location: index.php?uploadsuccessful");
            } else {
                echo "File too large";
            }
        } else {
            echo "An error has occurred";
        }
    } else {
        echo "Invalid file type";
    }
}
?>