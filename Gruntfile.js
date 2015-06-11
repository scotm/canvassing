module.exports = function (grunt) {
    require('time-grunt')(grunt);
    //require('jit-grunt')(grunt);

    // 1. All configuration goes here
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        criticalcss: {
            custom: {
                options: {
                    url: "http://127.0.0.1:8000",
                    width: 1200,
                    height: 900,
                    outputfile: "templates/critical.css",
                    filename: "css/main.css",
                    buffer: 800*1024,
                    ignoreConsole: false
                }
            }
        },

        cssmin: {
            options: {
                shorthandCompacting: true,
                roundingPrecision: -1
            },
            critical: {
                files: {
                  'templates/critical.min.css': ['templates/critical.css'],
                }
            },
            dist: {
                files: {
                  'css/main.min.css': ['css/main.css'],
                }
            },
        },

        concat: {

            dist: {
                src: [
                    'bower_components/jquery/dist/jquery.min.js',
                    //'bower_components/jquery-placeholder/jquery.placeholder.js',
                    'bower_components/jquery.cookie/jquery.cookie.js',
                    'bower_components/fastclick/lib/fastclick.js',
                    'bower_components/modernizr/modernizr.js',
                    'bower_components/leaflet/dist/leaflet.js',
                    //'bower_components/jquery-ui/jquery-ui.js',
                    'bower_components/jquery-ui/ui/core.js',
                    'bower_components/jquery-ui/ui/widget.js',
                    'bower_components/jquery-ui/ui/mouse.js',
                    'bower_components/jquery-ui/ui/sortable.js',
                    'bower_components/foundation/js/foundation/foundation.js', 
                    //'bower_components/foundation/js/foundation/foundation.abide.js', 
                    'bower_components/foundation/js/foundation/foundation.accordion.js', 
                    'bower_components/foundation/js/foundation/foundation.alert.js', 
                    //'bower_components/foundation/js/foundation/foundation.clearing.js', 
                    'bower_components/foundation/js/foundation/foundation.dropdown.js', 
                    //'bower_components/foundation/js/foundation/foundation.equalizer.js', 
                    //'bower_components/foundation/js/foundation/foundation.interchange.js', 
                    //'bower_components/foundation/js/foundation/foundation.joyride.js', 
                    //'bower_components/foundation/js/foundation/foundation.magellan.js', 
                    //'bower_components/foundation/js/foundation/foundation.offcanvas.js', 
                    //'bower_components/foundation/js/foundation/foundation.orbit.js', 
                    'bower_components/foundation/js/foundation/foundation.reveal.js', 
                    //'bower_components/foundation/js/foundation/foundation.slider.js', 
                    //'bower_components/foundation/js/foundation/foundation.tab.js', 
                    //'bower_components/foundation/js/foundation/foundation.tooltip.js', 
                    'bower_components/foundation/js/foundation/foundation.topbar.js', 
                    'js/accordion_mods.js'
                ],
                dest: 'js/production.js'
            },
            extras: {
                src: [
                    'bower_components/loadcss/loadCSS.js',
                    // 'bower_components/promise-polyfill/Promise.js'
                    // 'bower_components/fontfaceobserver/fontfaceobserver.js',
                    // 'js/extra_font_logic.js'
                ],
                dest: 'js/font_logic.js',
            },
        },

        uglify: {
            dist: {
                files: {
                    'js/production.min.js': 'js/production.js',
                }
            },
            font_logic_ugly: {
                files: {
                    'templates/extra_font_logic.min.js': 'js/font_logic.js',
                }
            }
        },

        imagemin: {
            dynamic: {
                files: [{
                    expand: true,
                    cwd: 'images/',
                    src: ['**/*.{png,jpg,gif}'],
                    dest: 'images/build/'
                }]
            }
        },

        sass: {
            options: {
                sourceMap: true,
                includePaths: ['bower_components/foundation/scss', 'static'],
                //outputStyle: 'compressed',
            },
            dist: {
                files: {
                    'css/main.css': 'scss/main.scss'
                }
            }
        },

        watch: {
            src: {
                files: ['lib/*.js', '!lib/dontwatch.js'],
                tasks: ['javascript']
            },
            sass: {
                files: ['scss/**.scss'],
                tasks: ['sass', 'cssmin:dist'],
                options: {
                    livereload: true
                }
            },
            html: {
                files: ['*/templates/**/*.html', '*/templates/*.html','templates/*.html'],
                options: {
                    livereload: true
                }
            }
        }
    });


    // 2. Where we tell Grunt we plan to use this plug-in.
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-imagemin');
    grunt.loadNpmTasks('grunt-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-criticalcss');
    grunt.loadNpmTasks('grunt-contrib-cssmin');

    // 3. Where we tell Grunt what to do when we type "grunt" into the terminal.
    grunt.registerTask('default', ['concat', 'uglify', 'sass', 'cssmin:dist']);
    grunt.registerTask('basecss', ['criticalcss', 'cssmin'])
    grunt.registerTask('images', ['imagemin']);
    grunt.registerTask('watch-changes', ['concat', 'uglify', 'imagemin', 'sass', 'watch']);
    grunt.registerTask('js', ['concat', 'uglify']);
    grunt.registerTask('css', ['sass', 'cssmin:dist']);
    grunt.registerTask('all', ['concat', 'uglify', 'sass', 'imagemin']);
};
