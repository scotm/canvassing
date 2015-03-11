module.exports = function (grunt) {

    // 1. All configuration goes here
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        concat: {
            dist: {
                src: [
                    'bower_components/jquery/dist/jquery.js',
                    'bower_components/jquery-placeholder/jquery.placeholder.js',
                    'bower_components/jquery.cookie/jquery.cookie.js',
                    'bower_components/fastclick/lib/fastclick.js',
                    'bower_components/modernizr/modernizr.js',
                    'bower_components/foundation/js/foundation.js',
                    'bower_components/leaflet/dist/leaflet-src.js',
                    //'bower_components/jquery-ui/jquery-ui.js',
                    'bower_components/jquery-ui/ui/core.js',
                    'bower_components/jquery-ui/ui/widget.js',
                    'bower_components/jquery-ui/ui/mouse.js',
                    'bower_components/jquery-ui/ui/sortable.js',
                    'js/accordion_mods.js'
                ],
                dest: 'js/production.js'
            }
        },

        uglify: {
            build: {
                src: 'js/production.js',
                dest: 'js/production.min.js'
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
                includePaths: ['bower_components/foundation/scss', 'static']
                //outputStyle: 'compressed'
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
                tasks: ['sass'],
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

    // 3. Where we tell Grunt what to do when we type "grunt" into the terminal.
    grunt.registerTask('default', ['concat', 'uglify', 'sass']);
    grunt.registerTask('images', ['imagemin']);
    grunt.registerTask('watch-changes', ['concat', 'uglify', 'imagemin', 'sass', 'watch']);
    grunt.registerTask('js', ['concat', 'uglify']);
    grunt.registerTask('css', ['sass']);
    grunt.registerTask('all', ['concat', 'uglify', 'sass', 'imagemin']);
};
