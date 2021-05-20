<?php
require_once __DIR__ . '/../vendor/autoload.php';
require_once __DIR__ . '/../db/example_database.php';
use \IMSGlobal\LTI;
$launch = LTI\LTI_Message_Launch::new(new Example_Database())
    ->validate();
$nrps = $launch->get_nrps();
$members = $nrps->get_members();
$username = "";
foreach ($members as $member) {
    if ($member["user_id"] == $launch->get_launch_data()["sub"]) {
        $username = $member["given_name"];
    }
}
$launch_id = $launch->get_launch_id();
var_dump($launch_id);
var_dump($username);
?>

<link href="static/breakout.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css?family=Gugi" rel="stylesheet">
<script>     console.log("breakpoint: 1")</script>

<?php

if ($launch->is_deep_link_launch()) {    
    ?>
    <div class="dl-config">
        <h1>Pick a Difficulty</h1>
        <ul>
            <li><a href="<?= TOOL_HOST ?>/configure.php?diff=easy&launch_id=<?= $launch->get_launch_id(); ?>">Easy</a></li>
            <li><a href="<?= TOOL_HOST ?>/configure.php?diff=normal&launch_id=<?= $launch->get_launch_id(); ?>">Normal</a></li>
            <li><a href="<?= TOOL_HOST ?>/configure.php?diff=hard&launch_id=<?= $launch->get_launch_id(); ?>">Hard</a></li>
        </ul>
    </div>
    <?php
    die;
}
?>

<script>     console.log("breakpoint: 2")</script>

<div id="game-screen">
    <div style="position:absolute;width:1000px;margin-left:-500px;left:50%; display:block">
        <div id="scoreboard" style="position:absolute; right:0; width:200px; height:486px">
            <h2 style="margin-left:12px;">Scoreboard</h2>
            <table id="leadertable" style="margin-left:12px;">
            </table>
        </div>
        <canvas id="breakoutbg" width="800" height="500" style="position:absolute;left:0;border:0;">
        </canvas>
        <canvas id="breakout" width="800" height="500" style="position:absolute;left:0;">
        </canvas>
    </div>
</div>

<script>     console.log("breakpoint: 3")</script>

<script>
    // Set game difficulty if it has been set in deep linking
    var curr_diff = "normal";
    var curr_user_name = "<?php echo $username ?>";
    var launch_id = "<?php echo $launch_id ?>";
</script>
<script type="text/javascript" src="static/breakout.js" charset="utf-8"></script>