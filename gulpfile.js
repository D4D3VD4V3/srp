var gulp = require("gulp");
var gshell = require("gulp-shell")

gulp.task("activatevenv", gshell.task(["source ~/.virtualenvs/venv/bin/activate"]))
gulp.task("runtests", gshell.task(["pytest"]))

gulp.task("watch", function(){
    gulp.watch(["./app/**/*.py"], ["runtests"]);});

gulp.task("default", ["runtests", "watch"]);
