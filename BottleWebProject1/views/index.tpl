% rebase('layout.tpl', title='Home Page', year=year)

<div class="container">
 <div class="row">
  <form action="/result" method="post" enctype="multipart/form-data">\
   
   <div class="form-group">
	<label for="csv_file">Zadaj CSV subor: </label>
	<input type="file" class="form-control-file" name = "csv_file" id="csv_file">	
   </div>
   
    
   
   <div class="form-group">
    <label class="col-form-label" for="first_hidden">Select number of neurons in first hidden layer:</label>
	<input type="text" class="form-control" id="first_hidden" name = "first_hidden" placeholder="First_hidden">
   </div>
   <div class="form-group">
    <label class="col-form-label" for="second_hidden">Select number of neurons in second hidden layer:</label>
	<input type="text" class="form-control" id="second_hidden" name = "second_hidden" placeholder="Second_hidden">
   </div>
   <div class="form-group">
    <label class="col-form-label" for="iteration">Select number of neurons in second hidden layer:</label>
	<input type="text" class="form-control" id="iteration" name = "iteration" placeholder="Iteration">
   </div>

     <button class="btn btn-primary" type="submit">Submit form</button>
  </form>
 </div>
</div>	

</div>



