$( document ).ready( function()  {
    console.log( $( "#accordion" ) );
    console.log( "abc");
   $( "#accordion" ).accordion({
       collapsible: true,
       heightStyle: "content", // Avoid that all have the same height
       active: false  // Start all closed
   });
});

//$(document).ready(function(){
//  $(document).on("click",".summary",function(){
//    $(this).next().toggleClass("show")
//  })
//});

//$( function() {
//   $( "#accordion" ).accordion({
//       collapsible: true,
//       heightStyle: "content", // Avoid that all have the same height
//       active: false  // Start all closed
//   });
//});
