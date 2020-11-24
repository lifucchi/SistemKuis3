{% extends "quiz/base.php" %}


{% block content %}

    {% for score in fullscore %}
    <div class="col-md-12">
                        <div class="card">
                          {% for indikatorscore in score.quiz_taker.all %}
                            <div class="card-body">
                                <div class="mx-auto d-block">
                                    <h5 class="text-sm-center mt-2 mb-1">{{indikatorscore.specific_competency.name}}</h5>
                                    <h5 class="text-sm-center mt-2 mb-1">nilai :  {{indikatorscore.desc}}</h5>
                                </div>
                                <!-- <hr> -->
                            </div>
                            {% endfor %}
                            <div class="card-footer">
                                <strong class="card-title mb-3">nilai total : {{score.score}}</strong>
                            </div>
                        </div>
    </div>


      {% endfor %}

{% endblock %}
