namespace Mapping.Glitch {
	[Name("Jump Slash Lift")]
	[Description("Reach areas using the jump slash that weren't intended.")]
	[Requires(Equipment.Sword)]
	public static JumpSlashLift;
}

namespace Mapping.Items {
	[Name("Chest Near South Clock Town Termina Entrance")]
	[Scene(Scene.SouthClockTown)]
	[Requires(Item.Hookshot)]
	[Glitchable(Glitch.JumpSlashLift)]
	public static SouthClockTownChestNearEntrance;
}

namespace Mapping.Scene {
	[SceneName("South Clock Town")]
	[SceneEntrances("East Clock Town", "North Clock Town", "West Clock Town", "Termina Field")]
	[SceneType(SceneType.MainArea)]
	public static Scene SouthClockTown;
}
