// Dedicated CI entry point for our fork. Leaves Unity process management to GameCI.
using UnityEditor.Build;

namespace OpenFusion.EditorTools
{
    public static class FusionFallCiBuild
    {
        public static void BuildAndroid()
        {
            if (!BuildScript.Build(false, "build/Android/FusionFall-Android-v0.1.0.apk"))
                throw new BuildFailedException("FusionFall Android APK build failed.");
        }
    }
}
