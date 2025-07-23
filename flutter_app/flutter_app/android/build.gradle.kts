//allprojects {
    //repositories {
      //  google()
    //    mavenCentral()
  //  }
//}
// Root level build.gradle
buildscript {
    repositories {
        google()
        mavenCentral()
        jcenter()
    }
    //dependencies {
      //  classpath 'com.android.tools.build:gradle:7.0.4'  // Or the version you're using
        //classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.5.21'  // If you're using Kotlin
    //}
}
allprojects {
    repositories {
        google()
        mavenCentral()
        jcenter()  // Optional
        //maven { url 'https://storage.googleapis.com/download.flutter.io' }
    }
}
val newBuildDir: Directory = rootProject.layout.buildDirectory.dir("../../build").get()
rootProject.layout.buildDirectory.value(newBuildDir)
subprojects {
    val newSubprojectBuildDir: Directory = newBuildDir.dir(project.name)
    project.layout.buildDirectory.value(newSubprojectBuildDir)
}
subprojects {
    project.evaluationDependsOn(":app")
}
tasks.register<Delete>("clean") {
    delete(rootProject.layout.buildDirectory)
}