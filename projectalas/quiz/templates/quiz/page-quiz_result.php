{% extends "quiz/base.php" %}


{% block content %}

      {% for score in fullscore %}
      <div class="col-md-12">
                          <div class="card">
                            <div class="card-header">
                                <strong class="text-sm-center">{{bcs.name}}</strong>
                            </div>

                            {% for indikatorscore in score.quiz_taker.all %}
                              <!-- <div class="card-body"> -->
                                  <!-- <div class="mx-auto d-block"> -->
                                      <!-- <h5 class="text-sm-center mt-2 mb-1">{{indikatorscore.specific_competency.base_Competency.name}}</h5> -->
                                      <!-- <h5 class="mt-2 mb-1">{{sc.name}}</h5> -->
                                      <!-- <h5 class=" mt-2 mb-1"></h5> -->
                                  <!-- </div> -->
                                  <!-- <hr> -->
                              <!-- </div> -->

                              <ul class="list-group list-group-flush">
                                      <li class="list-group-item">
                                          <a href="#">  {{indikatorscore.specific_competency.name}} <span class="badge badge-primary pull-right">nilai :  {{indikatorscore.desc}}</span></a>
                                      </li>
                                      <!-- <li class="list-group-item">
                                          <a href="#"> <i class="fa fa-tasks"></i> Recent Activity <span class="badge badge-danger pull-right">nilai :</span></a>
                                      </li>
                                      <li class="list-group-item">
                                          <a href="#"> <i class="fa fa-bell-o"></i> Notification <span class="badge badge-success pull-right">nilai :</span></a>
                                      </li>
                                      <li class="list-group-item">
                                          <a href="#"> <i class="fa fa-comments-o"></i> Message <span class="badge badge-warning pull-right r-activity">nilai :</span></a>
                                      </li> -->
                                  </ul>
                              {% endfor %}
                              <div class="card-footer">
                                  <strong class="card-title mb-3">nilai total : {{score.score}}</strong>
                              </div>
                          </div>
      </div>
        {% endfor %}

{% endblock %}
