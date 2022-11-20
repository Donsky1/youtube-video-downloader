for (let i=0; i < $URL_LENGTH; i++) {
    $('#save' + i).on('click', function(){
       $('#info' + i).addClass('loading').text('Загрузка...')
       url = $('#link' + i).val()
       console.log(url)
       $.ajax({
        url: 'download',
        method: 'POST',
        data:{'url': url},
        success: function(data){
            $('#info' + i).removeClass('loading').html('<b>СКАЧИВАНИЕ ЗАВЕРШЕНО</b>')
            $('#folder' + i).html('Папка загрузки: <b>' + data.file_path + '</b>')
        }
       })
    });
}
