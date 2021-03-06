var gulp = require("gulp")
var gshell = require("gulp-shell")
var rename = require("gulp-rename")

//gulp.task("activatevenv", gshell.task(["source ~/.virtualenvs/venv/bin/activate"]))
gulp.task("runtests", gshell.task(["pytest"]))
gulp.task("updaterequirements", gshell.task(["pip freeze > requirements.txt"]))

gulp.task("updatedockerignore", function(){
    gulp.src(".gitignore")
    .pipe(rename("./.dockerignore"))
    .pipe(gulp.dest("./"))})

gulp.task("watch", function(){
    gulp.watch(["./app/**/*.py"], ["runtests"])})

gulp.task("default", ["watch", "runtests", "updaterequirements", "updatedockerignore"])
