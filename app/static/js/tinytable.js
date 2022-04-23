function tinytablefunc(inputsearch) {



$(document).ready(function () {


  //'{{ searchstring}}'
  //alert(searchstring)

  // DataTable
  var tablet = $(document).ready( function () {
      $('#datatable').DataTable({
      ajax: '/vault/api/part',
      //dom: 'Bfrtip',
      serverSide: true,
      deferRender: true,
      processing: true,
      lengthMenu: [ [10, 25, 50,100,250], [10, 25, 50,100,250] ],
      oSearch: {"sSearch": inputsearch},
      columns: [
              
              {data: 'pngpath', orderable: false},
              {data: 'partnumber', class: 'editable text'},
              {data: 'revision'},
              {data: 'description', class: 'editable text'},
              {data: 'process'},
              {data: 'finish', class: 'editable text'},
              {render: function (data, type, row) {    
                    return [createButton('edit', row.id),createButton('delete', row.id)];    
                }},
            ],



        initComplete: function () {
            // Apply the search

            this.api().columns().every( function () {
                var that = this;

                $( 'input', this.footer() ).on( 'keyup change clear', function () {
                    if ( that.search() !== this.value ) {
                        that
                            .search( this.value )
                            .draw();
                    }
                } );
            } );
        }
    });
  });


          // Setup - add a text input to each footer cell
       $('#datatable tfoot th').each( function () {
      var title = $(this).text();
      if ( title !== 'Preview' && title !== 'Action' ) {
        $(this).html( '<input type="text" placeholder="Search '+title+'" style="width:100px"/>' );
                  } 
      
  } );
      


function createButton(buttonType, rowID) {    
  var buttonText = buttonType == "edit" ? "Edit" : "Delete";  
  //var onclickAction==  
  return '<button class="' + buttonType + '" type="button" >' + buttonText+'</button>';    
} 

    
function fnCreateTextBox(value, fieldprop) {    
  return '<input data-field="' + fieldprop + '" type="text" value="' + value + '" ></input>';    
} 



function fnUpdateDataTableValue($inputCell, value) {    
  var dataTable = $('#datatable').DataTable();    
  var rowIndex = dataTable.row($($inputCell).closest('tr')).index();   
  console.log(value, rowIndex, $inputCell) 
  
  var fieldName = $($inputCell).attr('data-field');

  console.log(fieldName,value)
  
  dataTable.rows().data()[rowIndex][fieldName] = value; 
}    






function fnCreateTextBox(value, fieldprop) {    
      return '<input data-field="' + fieldprop + '" type="text" value="' + value + '" ></input>';    
  } 
 
  
function fnResetControls() {    
      var openedTextBox = $('#datatable').find('input');    
      $.each(openedTextBox, function (k, $cell) {    
          $(openedTextBox[k]).closest('td').html($cell.value);    
      })    
  } 


$('#datatable').on('click', 'tbody td .cancel', function (e) {    
      fnResetControls();    
      $('#datatable tbody tr td .update').removeClass('update').addClass('edit').html('Edit');    
      $('#datatable tbody tr td .cancel').removeClass('cancel').addClass('delete').html('Delete');    
  });    

$('#datatable').on('click', 'tbody td .update', function (e) {    

  var openedTextBox = $('#datatable').find('input');
  var dataTable = $('#datatable').DataTable(); 

  var partid;
  var partnumber;
  var description ;
  var revision;
  var process;
  // var process2;
  // var process3;
  var finish
  
  var rowref;
  var colref;

  $.each(openedTextBox, function (k, $cell) { 
      if ($cell.placeholder == '') {
      console.log($cell.placeholder)
      
      fnUpdateDataTableValue($cell, $cell.value);
      rowref = dataTable.row($($cell).closest('tr')).index();  
      colref= dataTable.column($($cell).closest('td')).index();  
      //console.log("rowindex ",rowref,"colindex ",colref) 
      

      $(openedTextBox[k]).closest('td').html($cell.value);  
     
      
      if (colref == 1) {
          partnumber = $cell.value;
          
      }
       else if (colref == 2) {
          revision = $cell.value;}   
         else if (colref == 3) {
          description = $cell.value;}
          else if (colref == 4) {
          process = $cell.value;} 
          // else if (colref == 5) {
          // process2 = $cell.value;}
          // else if (colref == 6) {
          // process3 = $cell.value;}
          else if (colref == 5) {
          finish = $cell.value;}
                  
      //console.log(jobid,jobnumber,description,customer)     
      
      
      }

  })  


  console.log("updated ", dataTable.rows(rowref).data()[0]);
  partnumber = dataTable.rows(rowref).data()[0]['partnumber'];
  revision = dataTable.rows(rowref).data()[0]['revision'];


  var data_tosend={partnumber:partnumber,description:description,
                    revision:revision, process:process,  finish:finish}
  console.log(partid,partnumber,revision,description,revision,process,finish);   
  console.log(data_tosend);     
  
  console.log("sent data is before?")

  
  var sel_row = dataTable.row( $(this).parents('tr') );


  $('#datatable tbody tr td .update').removeClass('update').addClass('edit').html('Edit');    
  $('#datatable tbody tr td .cancel').removeClass('cancel').addClass('delete').html('Delete');  
  
      //send the data back to database

  //var sel_row = $cell;
  // var data_tosend=sel_row.data();

  $.ajax({
      type: "POST",
      url: 'partapi/update',
      dataType: "json",
      data: data_tosend,
      //data: $(clickedRow),

      success: function(response) {
          console.log(response);
      },
      error: function(error) {
           console.log(error);
      }
  });
  

  dataTable.draw();




  });  


$('#datatable').on('click', 'tbody td .delete', function (e) {    
      fnResetControls();    


      var tablon = $('#datatable').DataTable();    
      var clickedRow = $($(this).closest('td')).closest('tr');  
      var sel_row = tablon.row( $(this).parents('tr') );
      var data_tosend=sel_row.data();

      console.log(data_tosend['partnumber'])

      var test="dklfsdlkfs";
     

      // var retVal = confirm($(data_tosend['partnumber']));
      // if( retVal == true ){
      var retVal = confirm("Confirm to delete: "+ data_tosend['partnumber'] + " revision "+ data_tosend['revision'] );
             if( retVal == true ){

             


      $.ajax({
          type: "POST",
          url: 'partapi/delete',
          dataType: "json",
          data: data_tosend,
          //data: $(clickedRow),

          success: function(response) {
              // console.log($(clickedRow));
              //console.log( $(test));
              console.log(response);
          },
          error: function(error) {
              //console.log( $(test));
              console.log(error);
          }
      });


      //Erase the row
      tablon.row($(clickedRow)).remove().draw();
      
      }
  });  



$('#datatable').on('click', 'tbody td .edit', function (e) {    
  fnResetControls();    
  var dataTable = $('#datatable').DataTable();    
  var clickedRow = $($(this).closest('td')).closest('tr');    
  

  $(clickedRow).find('td').each(function () {    
      // do your cool stuff    
      if ($(this).hasClass('editable')) {    
          if ($(this).hasClass('text')) {    
              var html = fnCreateTextBox($(this).html(), 'name');    
              $(this).html($(html))  
              console.log(this.type)      
          }    
      }    
  });     
  
  
  $('#datatable tbody tr td .update').removeClass('update').addClass('edit').html('Edit');    
  $('#datatable tbody tr td .cancel').removeClass('cancel').addClass('delete').html('Delete');    
  $(clickedRow).find('td .edit').removeClass('edit').addClass('update').html('Update');    
  $(clickedRow).find('td .delete').removeClass('delete').addClass('cancel').html('Cancel');    
 
});        




      });


     
    }