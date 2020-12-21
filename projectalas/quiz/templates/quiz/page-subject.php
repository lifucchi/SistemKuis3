{% extends "quiz/base.php" %}
      {% block content %}
      <div class="row">

        {% for s in subject_list %}

          <div class="col-md-4">
            <!-- <div class="card"> -->
                <!-- <div class="card-header" style="background-color:#dbc1ac;"> -->
                    <!-- <strong class="card-title">{{s.name}}</strong> -->
                <!-- </div> -->
                <!-- <div class="card-body"> -->
                    <!-- <button onclick="window.location.href = '{{s.id}}';" type="button" class="button-default cart-btn">Read More</button> -->
                    <!-- <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p> -->
                    <!-- <button onclick="window.location.href = 'kelas/{{s.id}}';" type="button" class="btn btn-primary" style="float: right;"><i class="fa fa-star"></i>&nbsp;Selengkapnya</button> -->
                    <!-- <button onclick="location.href = '{% url 'classes' pk=s.id %}';" type="button" class="btn btn-coklat"  style="float: right;"><i class="fa fa-star"></i>&nbsp;Selengkapnya</button> -->

                <!-- </div> -->
            <!-- </div> -->

            <div class="card">
                            <div class="card-body">
                                <div class="mx-auto d-block">
                                    <h2 class="text-sm-center mt-2 mb-1">{{s.name}}</h2>

                                </div>
                                <hr>
                            </div>
                            <div class="card-body text-center" style="background-color:#dbc1ac;"   >
                              <button   onclick="location.href = '{% url 'classes' pk=s.id %}';" type="button" class="btn btn-coklat center"  ><i class="fa fa-star"></i>&nbsp;Selengkapnya</button>
                            </div>
                        </div>
        </div>

      {% endfor %}

      </div>

{% endblock %}
