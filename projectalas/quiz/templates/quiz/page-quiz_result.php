{% extends "quiz/base.php" %}


{% block content %}

      {% for score in fullscore %}
      <div class="col-md-12">
                          <div class="card">
                            <div class="card-header" >
                                <strong class="text-sm-center">{{bcs.name}}</strong>
                            </div>

                            {% for indikatorscore in score.quiz_taker.all %}


                              <ul class="list-group list-group-flush">
                                      <li class="list-group-item">
                                          <a href="#">  {{indikatorscore.specific_competency.name}} <span class="badge badge-primary pull-right">nilai :  {{indikatorscore.desc}}</span></a>
                                      </li>
                                  </ul>
                              {% endfor %}
                              <div class="card-footer" style="background-color:#967259;">
                                  <strong class="card-title mb-3" style="color:#ece0d1">nilai total : {{score.score}}</strong>
                              </div>
                          </div>
      </div>
        {% endfor %}
        <div class="card-body text-center" style="background-color:#dbc1ac;"   >

        <button   onclick="location.href = '{% url 'subjects' %}';" type="button" class="btn btn-coklat center"  ><i class="fa fa-star"></i>&nbsp;Beranda</button>
      </div>


{% endblock %}
