function selectpart(jobnumber) {

    console.log(jobnumber);

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
      
      columns: [
              
              {data: 'pngpath', orderable: false},
              {data: 'partnumber', class: 'editable text'},
              {data: 'revision'},
              {data: 'description', class: 'editable text'},
              {data: 'process'},
              {data: 'finish', class: 'editable text'},
              {render: function (data, type, row) {    
                    return '<button class="' + "add" + '" type="button" >' + "Add part"+'</button>';    
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
      







$('#datatable').on('click', 'tbody td .add', function (e) {    
      


      var tablon = $('#datatable').DataTable();    
      var clickedRow = $($(this).closest('td')).closest('tr');  
      var sel_row = tablon.row( $(this).parents('tr') );
      var data_tosend=sel_row.data();

      data_tosend['jobnumber']=jobnumber;

      console.log("ssendata"+data_tosend['jobnumber'])

      console.log(data_tosend)



      $.ajax({
          type: "POST",
          url: '/vault/jobapi/addtobom',
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


      
      
  });  




      });
     
    }