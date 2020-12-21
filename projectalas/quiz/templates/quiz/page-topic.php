{% extends "quiz/base.php" %}
      {% block content %}



      <div class="row">

        {% for bc in bcs %}



          <div class="col-lg-12">
            <div class="card">
                <div class="card-header" style="background-color:#967259;">
                    <strong class="card-title" style="color:#ece0d1">{{ topic_name }}</strong>
                </div>
                <div class="card-body">
                  <p class="card-text" style="color:black">Kompetensi Dasar </p>
                  <p class="card-text">{{bc.name}}</p>
                  <hr>
                  <p class="card-text" style="color:black">Indikator </p>
                  {% for indikator in bc.k_dasar.all %}
                    <p class="card-text">  {{indikator.name}}</p>
                  {% endfor %}
                  <hr>


                  <!-- <button type="button" class="btn btn-success mb-1" data-toggle="modal" data-target="#largeModal">Large</button> -->
                  {% if bc.roll_out == 1 %}
                  <button onclick="location.href = '{% url 'take_quiz' pk=bc.pk %}';" type="button" class="btn btn-success" style="float: right;"><i class="fa fa-star"></i>&nbsp;Mulai Kuis</button>
                  <button onclick="location.href = '{% url 'scores' pk=bc.pk %}';" type="button" class="btn btn-success "  style="float: left;"><i class="fa fa-magic"></i>&nbsp;Nilai</button>
                  <button  type="button" class="btn btn-danger" data-toggle="modal"  data-target="#largeModal"  style="float: right;">Petunjuk Pengerjaan</button>

                  {% else %}
                  <button onclick="location.href = '{% url 'take_quiz' pk=bc.pk %}';" type="button" class="btn btn-success "  disabled="" style="float: right;"><i class="fa fa-star"></i>&nbsp;Mulai Kuis</button>
                  <button onclick="location.href = '';" type="button" class="btn btn-success "  disabled=""  style="float: left;"><i class="fa fa-magic"></i>&nbsp;Nilai</button>
                  <button  type="button" class="btn btn-danger" data-toggle="modal"  data-target="#largeModal"  disabled=""  style="float: right;">Petunjuk Pengerjaan</button>

                  <!-- <button type="button" class="btn btn-success mb-1" data-toggle="modal" data-target="#largeModal">Large</button> -->
                  {% endif %}


                </div>
            </div>
        </div>

        <div class="modal fade" id="largeModal" tabindex="-1" role="dialog" aria-labelledby="largeModalLabel" aria-hidden="true">
          <div class="modal-dialog modal-lg" role="document">
              <div class="modal-content">
                  <div class="modal-header">
                      <h5 class="modal-title" id="largeModalLabel">Petunjuk Pengerjaan Kuis</h5>
                      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                          <span aria-hidden="true">&times;</span>
                      </button>
                  </div>
                  <div class="modal-body">
                      <p>
                            1.Berdo’alah sebelum mengerjakan!
                            <br>
                            2.Soal yang diberikan berupa pilihan ganda
                            <br>
                            3.Periksa dan bacalah soal-soal dengan saksama sebelum Anda menjawabnya.
                            <br>
                            4.Jumlah butir soal yang diberikan sesuai dengan kemampuan atau maksimal sebanyak 6 soal pada setiap indikator
                      </p>
                  </div>
                  <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                  </div>
              </div>
          </div>
      </div>

      {% endfor %}

      </div>



{% endblock %}
