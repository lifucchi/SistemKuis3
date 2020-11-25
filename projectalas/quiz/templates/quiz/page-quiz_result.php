{% extends "quiz/base.php" %}


{% block content %}
    {% for bc in bcs %}
    <div class="col-md-12">
                        <div class="card">
                          <div class="card-header">
                              <strong class="text-sm-center">{{ bc.name }}</strong>
                          </div>

                          {% for sc in bc.k_dasar.all %}
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
                                        <a href="#">  {{sc.name}} <span class="badge badge-primary pull-right">{% for d in sc.indikators.all %} nilai : {{d.desc}} {% endfor %}</span></a>
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
                                <strong class="card-title mb-3"></strong>
                            </div>
                        </div>
    </div>
      {% endfor %}

{% endblock %}
