<script>
function delblog(){
	const ans = confirm("确认要删除？");
	if (ans===false) {
		event.preventDefault(); //取消默认应答
       return false;
    }else{
    	alert("删除成功")
    	return true
    }

}
</script>