{% load static %}

<!doctype html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang=""> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8" lang=""> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9" lang=""> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang=""> <!--<![endif]-->
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>SistemKuis</title>

    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="apple-touch-icon" href="https://i.imgur.com/kSe3GEP.png">
    <link rel="shortcut icon" href="https://i.imgur.com/kSe3GEP.png">

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/normalize.css@8.0.0/normalize.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/lykmapipo/themify-icons@0.1.2/css/themify-icons.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pixeden-stroke-7-icon@1.2.3/pe-icon-7-stroke/dist/pe-icon-7-stroke.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/3.2.0/css/flag-icon.min.css">
    <link rel="stylesheet" href="{% static 'assets/css/cs-skin-elastic.css'%}">
    <link rel="stylesheet" href="{% static 'assets/css/style.css'%}">

   <style>


      .btn-coklat {
        color: #FFFFFF;
        background-color: #634832;
        border-color: #130269;
      }

      .btn-coklat:hover,
      .btn-coklat:focus,
      .btn-coklat:active,
      .btn-coklat.active,
      .open .dropdown-toggle.btn-coklat {
        color: #FFFFFF;
        background-color: #38220f;
        border-color: #130269;
      }

      .btn-coklat:active,
      .btn-coklat.active,
      .open .dropdown-toggle.btn-coklat {
        background-image: none;
      }

      .btn-coklat.disabled,
      .btn-coklat[disabled],
      fieldset[disabled] .btn-coklat,
      .btn-coklat.disabled:hover,
      .btn-coklat[disabled]:hover,
      fieldset[disabled] .btn-coklat:hover,
      .btn-coklat.disabled:focus,
      .btn-coklat[disabled]:focus,
      fieldset[disabled] .btn-coklat:focus,
      .btn-coklat.disabled:active,
      .btn-coklat[disabled]:active,
      fieldset[disabled] .btn-coklat:active,
      .btn-coklat.disabled.active,
      .btn-coklat[disabled].active,
      fieldset[disabled] .btn-coklat.active {
        background-color: #634832;
        border-color: #130269;
      }

      .btn-coklat .badge {
        color: #634832;
        background-color: #FFFFFF;
      }


    </style>
</head>

<body class="open" style="background-color:#ece0d1;">
    <!-- Left Panel -->
    <aside id="left-panel" class="left-panel" style="background-color:#dbc1ac;">
        <nav class="navbar navbar-expand-sm navbar-default"  style="background-color:#dbc1ac;" >
            <div id="main-menu" class="main-menu collapse navbar-collapse">
                <ul class="nav navbar-nav">
                    <li class="">
                        <a style="color:black" onclick="return confirm('Apa anda yakin? Data akan hilang?')" href=" {% url 'subjects'%} "><i style="color:black" class="menu-icon fa fa-laptop"></i>Mata Pelajaran </a>
                    </li>


                </ul>
            </div><!-- /.navbar-collapse -->
        </nav>
    </aside>
    <!-- /#left-panel -->
    <!-- Right Panel -->
    <div id="right-panel" class="right-panel" style="background-color:#ece0d1;">
        <!-- Header-->
        <header id="header" class="header" style="background-color:#634832;">
            <div class="top-left" style="background-color:#634832;">
                <div class="navbar-header" style="background-color:#634832;">
                    <!-- <a onclick="return confirm('Apa anda yakin? Data akan hilang?')" class="navbar-brand" href="">SistemKuis</a> -->
                    <h2 class="navbar-brand" style="color:#fff" >SistemKuis</h2>
                    <!-- <a class="navbar-brand" href="">  SistemKuis</a> -->
                    <a id="menuToggle" class="menutoggle"><i class="fa fa-bars"></i></a>

                </div>


            </div>
            <!-- <div class="top-left"> -->
                <!-- <div class="navbar-header"> -->
                    <!-- <a class="navbar-brand" href="./">Mata Pelajaran</a> -->
                    <!-- <a class="navbar-brand" href="">  SistemKuis</a> -->
                    <!-- <a id="menuToggle" class="menutoggle"><i class="fa fa-bars"></i></a> -->

                <!-- </div> -->

            <!-- </div> -->

            <div class="top-right">
                <div class="header-menu">
                    <div class="header-left">


                        <div class="user-area dropdown float-right">
                          {% if user.is_authenticated %}


                            <a href="#" class="dropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="color:#fff">
                                <!-- <img class="user-avatar rounded-circle" src="images/admin.jpg" alt="User Avatar"> -->
                                {{ user.first_name }} {{ user.last_name }}
                                <i class="fa fa- user"></i><span class="ti-angle-down"></span>

                            </a>

                            <div class="user-menu dropdown-menu" >
                                <a style="color:black" class="nav-link" href="#"><i class="fa fa-user"></i>{{ user.username }}</a>

                                <a style="color:black" class="nav-link" href="#"><i class="fa fa-cog"></i>Kelas {{ user.classes }}</a>

                                <a style="color:black" onclick="return confirm('Apa anda yakin? Data akan hilang')" class="nav-link" href="{% url 'logout'%}"><i class="fa fa-power-off"></i>Logout</a>
                            </div>
                        </div>
                        {% else %}
                        {% endif %}

                    </div>



                </div>
            </div>
        </header>
        <!-- /#header -->
        <!-- Content -->
        <div class="content">
          {% block content %} {% endblock %}
                <div class="clearfix"></div>
        </div>
        <div class="clearfix"></div>
        <div class="clearfix"></div>

    </div>
    <script src="https://cdn.jsdelivr.net/npm/jquery@2.2.4/dist/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.4/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/js/bootstrap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/jquery-match-height@0.7.2/dist/jquery.matchHeight.min.js"></script>
    <script src="{% static 'assets/js/main.js'%}"></script>


    <script>
        jQuery(document).ready(function($) {

        });
    </script>
</body>
</html>
