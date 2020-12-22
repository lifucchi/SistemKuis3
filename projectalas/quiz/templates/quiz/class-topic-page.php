{% extends "projectalas/base.php" %}
      {% block content %}
      <div class="edu-accordion-area mg-b-15">
          <div class="container-fluid">
              <div class="row">
                  <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" >
                      <div class="tab-content-details mg-b-30">
                          <h2>{{topics.name}}</h2>
                      </div>
                  </div>
              </div>

              <div class="row">
                  {% for bc in bcs %}
                <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                    <div class="courses-inner res-mg-b-30">
                        <h5>{{bc.name}}</h5>
                        <br>
                        <button onclick="" type="button" class="btn-danger cart-btn">Start Quiz</button>
                    </div>
                    <br>
                </div>

                  {% endfor %}
          </div>
      </div>
    </div>
{% endblock %}
