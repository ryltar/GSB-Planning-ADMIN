var grid = $("#grid-employee").bootgrid({
  labels:{
    infos: "Affichage de l'élément {{ctx.start}} à {{ctx.end}} sur un total de {{ctx.total}} éléments",
    search: "Recherche"
  },
  ajax: true,
  rowSelect: true,
  sorting: true,

  post: function ()
  {
    /* To accumulate custom parameter with the request object */
    return {
      id: "b0df282a-0d67-40e5-8558-c9e93b7befed"
    };
  },

  url: "/loadEmployee",

  formatters: {
    "commands": function(column, row)
    {
      return "<button type=\"button\" class=\"btn btn-xs btn-default command-edit\" data-row-id=\"" + row.id + "\"><span class=\"fa fa-pencil\"></span></button> " +
      "<button type=\"button\" class=\"btn btn-xs btn-default command-delete\" data-row-id=\"" + row.id + "\"><span class=\"fa fa-trash-o\"></span></button>";
    }
  }

}).on("loaded.rs.jquery.bootgrid", function()
{
  grid.find(".command-edit").on("click", function(e)
  {
    var ele =$(this).parent();
    if($(this).data("row-id") > 0) {
      $('#edit_model').modal('show');
      $('#edit_id').val(ele.siblings(':first').html());
      if(ele.siblings(':nth-of-type(2)').html() == 'true'){
        $('#edit_admin')[0].options[0].setAttribute("selected", "selected")
      }else{
        $('#edit_admin')[0].options[1].setAttribute("selected", "selected")
      }
      $('#edit_lastname').val(ele.siblings(':nth-of-type(3)').html());
      $('#edit_firstname').val(ele.siblings(':nth-of-type(4)').html());
      $('#edit_pseudo').val(ele.siblings(':nth-of-type(5)').html());
      $('#edit_email').val(ele.siblings(':nth-of-type(6)').html());
      $('#edit_phone').val(ele.siblings(':nth-of-type(7)').html());

    } else {
      alert('First select row, then click edit button');
    }
  }).end().find(".command-delete").on("click", function(e){
    var conf = confirm("Voulez vous supprimer l'item n° " + $(this).data("row-id") );
    if(conf){
      $(this).parent().parent().remove();
      $("#grid-employee").bootgrid('remove', $(this).data("row-id"))
      $.ajax({
        url:'/deleteEmployee',
        type:'DELETE',
        data: 'id=' + $(this).data("row-id"),
      })  
    }
  })
});

$( "#btn_edit" ).click(function(){
  $.ajax({
    url:'/editEmployee',
    type:'PUT',
    data: $('#frm_edit').serialize(),
  })

  grid.bootgrid("reload")

});



