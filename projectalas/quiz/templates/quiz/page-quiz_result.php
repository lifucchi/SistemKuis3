{% extends "quiz/base.php" %}


{% block content %}
<div class="col-md-4">
                <aside class="profile-nav alt">
                    <section class="card">
                        <!-- <div class="card-header user-header alt bg-dark">
                            <div class="media">
                                <a href="#">
                                    <img class="align-self-center rounded-circle mr-3" style="width:85px; height:85px;" alt="" src="images/admin.jpg">
                                </a>
                                <div class="media-body">
                                    <h2 class="text-light display-6">Jim Doe</h2>
                                    <p>Project Manager</p>
                                </div>
                            </div>
                        </div> -->


                        <ul class="list-group list-group-flush">

                          {% for ind in indikatorscore %}

                            <li class="list-group-item">
                                 {{ind.id}} <i></i> {{ ind.desc }}
                            </li>
                        </ul>
                          {% endfor %}

                          <li class="list-group-item">
                               Total <i></i> {{ indikatornext }}
                          </li>

                    </section>
                </aside>
            </div>
{% endblock %}

{% extends "quiz/base.php" %}


{% block content %}
    {% for score in fullscore %}
              {% for indikatorscore in score.quiz_taker.all %}
              <br>
                  ini nama indikator {{indikatorscore.specific_competency_id}}
                  <br>
                  ini nilai perindikator {{indikatorscore.desc}}
              {% endfor %}
              <br>
              ini nilai total {{score.score}}
    {% endfor %}
{% endblock %}
