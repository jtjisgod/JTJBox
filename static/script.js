$(function() {
    $("#btn_search").click(btn_search);
});


function btn_search() {
    var targetName = $("#ipt_name").val();
    var targetUrl = $("#ipt_url").val();
    if(!targetName) {
        alert("Please insert target's name.");
        return;
    }
    if(!targetUrl) {
        alert("Please insert target's url.");
        return;
    }
    var url = "/update/crawling?name=" + targetName + "&url=" + targetUrl;
    $("#loading").show();
    $.ajax({
        url: url,
        type: "get",
        success:function(res) {
            $("#loading").hide();
            res = JSON.parse(res);
            if(res.status == "success") {
                location.href = "/detail/" + res.code;
                return;
            }
            alert(res.message);
            return;
        }
    });
}