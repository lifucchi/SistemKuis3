{% extends "users/base.php" %}
      {% block content %}
        <div class="courses-area">
            <div class="container-fluid">
                <div class="row">

                  {% for t in topic_list %}

                      <div class="col-lg-3 col-md-6 col-sm-6 col-xs-12">
                          <div class="courses-inner res-mg-b-30">
                              <div class="courses-title">
                                <h2>{{ t.name }}</h2>
                                <!-- <h2>{{ t.topictopic }}</h2> -->

                              </div>
                              <div class="product-buttons">
                                  <button onclick="window.location.href = '{{t.slug}}';" type="button" class="button-default cart-btn">Read More</button>
                              </div>
                          </div>
                      </div>
                  {% endfor %}



                </div>

              <br>
            </div>
        </div>


{% endblock %}
